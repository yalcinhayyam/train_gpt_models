/* eslint-disable react/prop-types */
import { useState, useEffect, useMemo } from "react";
import "./App.scss";
import axios from "axios";
import Markdown from "react-markdown";

const configs = [
  { model: "llama-default", answeredBy: "LLama", border: "ring-emerald-400" },
  {
    model: "bard",
    answeredBy: "Bard",
    border: "ring-lime-400",
  },
  {
    model: "gemini-pro",
    answeredBy: "Gemini-Pro",
    border: "ring-rose-400",
  },
  {
    model: "gpt-3.5-turbo",
    answeredBy: "Gpt-3.5-Turbo",
    border: "ring-fuchsia-400",
  },
  {
    model: "gpt-4",
    answeredBy: "Gpt-4",
    border: "ring-blue-400",
  },
];
const questions = [
  {
    title: "Görme Bozukluğu",
    query: "Bulanık ve çatallı görmeye başladım",
  },
  {
    title: "Baş Ağrısı",
    query: "Sürekli baş ağrısı çekiyorum",
  },
];

function App() {
  // const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [useRetrievalAG, setUseRetrievalAG] = useState(false);
  const [value, setValue] = useState(null);
  const [loading, setLoading] = useState(false);
  const showQuestion = useMemo(() => results.length == 0, [results]);
  // const queryRef = useRef(null);
  const ask = async (model, query) => {
    const start = Date.now();
    const result = await axios.post(
      `http://127.0.0.1:8000/${useRetrievalAG ? "rag" : "ask"}`,
      {
        model: model,
        message: query,
      }
    );

    const finish = Date.now();
    const time = (finish - start) / 1000;
    return { ...result, time };
  };

  const handle = async (query) => {
    const models = configs.length;
    let count = 0;
    const cleanUp = () => {
      count++;
      if (count == models) {
        setLoading(false);
        setValue(null);
        count = 0;
      }
    };
    setResults([]);
    setLoading(true);
    configs.forEach((config) => {
      ask(config.model, query)
        .then((res) => {
          cleanUp();
          setResults((prev) => [
            {
              query,
              message: res.data.result,
              time: res.time,
              border: config.border,
              answeredBy: config.answeredBy,
            },
            ...prev,
          ]);
        })
        .catch((err) => {
          console.log(err);
          cleanUp();
        });
    });
  };

  return (
    <>
      <main className="flex container md:max-w-[900px] mx-auto px-4 justify-center pt-5">
        <div className="flex container flex-col">
          <div className="flex justify-between">
            <h2 className="card-title">Whats My Problem!</h2>
            <label className="cursor-pointer label w-44 font-bold">
              <span className="label-text">Use Retrieval AG</span>

              <input
                type="checkbox"
                className="toggle toggle-info border-2"
                checked={useRetrievalAG}
                onChange={(e) => setUseRetrievalAG(e.target.checked)}
              />
            </label>
          </div>

          <Query
            handle={handle}
            setValue={setValue}
            value={value}
            loading={loading}
          />
          <div>
            {showQuestion && (
              <>
                {questions.map((question, index) => (
                  <Question
                    key={index}
                    title={question.title}
                    query={question.query}
                    handle={handle}
                  />
                ))}
              </>
            )}
          </div>
          <div>
            {results.map((result, index) => (
              <Response key={index} {...result} />
            ))}
          </div>
        </div>
      </main>
    </>
  );
}
function Question({ title, query, handle }) {
  return (
    <div role="alert" className="alert shadow-lg mt-5 bg-slate-950">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        className="stroke-info shrink-0 w-6 h-6"
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth="2"
          d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
        ></path>
      </svg>
      <div>
        <h3 className="font-bold">{title}!</h3>
        <div className="text-xs">{query}</div>
      </div>
      <button
        className="btn btn-sm btn-info"
        onClick={() => {
          handle(query);
        }}
      >
        Sebebini Hemen Öğren
      </button>
    </div>
  );
}

//  * @param {{queryRef:React.MutableRefObject<HTMLTextAreaElement> ,handle:Function}} props
/**
 * @param {{setValue: React.Dispatch<React.SetStateAction<null>>,value?:string,handle:Function}} props
 */
function Query({ setValue, value, handle, loading }) {
  const [disabled, setDisabled] = useState(true);
  useEffect(() => {
    if (value?.length > 0) {
      setDisabled(false);
    } else {
      setDisabled(true);
    }
  }, [value]);

  return (
    <label className="mt-5 w-full flex relative">
      {loading ? (
        <span className="loading loading-spinner absolute right-4 bottom-3"></span>
      ) : (
        <button
          className="btn btn-ghost absolute right-1 bottom-0 btn-link"
          disabled={disabled}
          onClick={() => handle(value)}
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            strokeWidth={1.5}
            stroke="currentColor"
            className="w-6 h-6"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M6 12 3.269 3.125A59.769 59.769 0 0 1 21.485 12 59.768 59.768 0 0 1 3.27 20.875L5.999 12Zm0 0h7.5"
            />
          </svg>
        </button>
      )}

      <textarea
        // ref={queryRef}
        onChange={(e) => setValue(e.target.value)}
        className="textarea textarea-bordered h-0 w-full"
        placeholder="Sorununuz nedir?"
        onKeyDown={(e) => {
          if (e.keyCode === 13 && e.shiftKey === false) {
            e.preventDefault();
            if (!disabled) {
              handle(value);
            }
          }
        }}
      ></textarea>
    </label>
  );
}
// eslint-disable-next-line react/prop-types
function Response({ answeredBy, message, border, query, time }) {
  return (
    <div className={`card m-2 bg-base-100 mt-4 shadow-xl ring-2 ${border}`}>
      <div className="card-body">
        <h2 className="card-title text-primary">{answeredBy}!</h2>
        <Markdown>{message}</Markdown>
        <div className={`divider divider-start text-purple-50`}>
          Cevaplanan Soru
        </div>
        {query}
        <div className="card-actions justify-end">
          <div className="badge badge-outline font-medium border-2 p-3">
            {new Date().toLocaleString("tr-TR")}
          </div>
          <div
            className={`badge badge-outline badge-info font-medium border-2 p-3`}
          >
            {time} saniye
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
