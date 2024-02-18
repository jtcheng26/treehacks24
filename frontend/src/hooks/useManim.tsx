import { QuizConfig } from "@/components/content/Content";
import { MCQuestionConfig } from "@/components/practice/MCQuizQuestion";
import { TextQuestionConfig } from "@/components/practice/TextQuizQuestion";
import { fetchr, getStoryboards } from "@/components/requests/post";
import { useCallback, useEffect, useRef, useState } from "react";

/*
TODO: do the parentheses
Request all sections (show content once first ready)
set ready to true
when updating, insert new section (and re-render all after sections)
*/

export interface Section {
  title: string;
  id: string;
  progressState: {
    // frontend
    played: number;
    loaded: number;
    playedSeconds: number;
    loadedSeconds: number;
  };
  question: {
    // from backend
    type: "mc" | "text" | "skip";
    data: MCQuestionConfig | TextQuestionConfig; // or other types
  };
  video: string; // or stream, from backend
  ready: boolean; // frontend
}

export interface SectionList {
  sections: Section[];
  ready: boolean;
}

const initialProgressState = {
  played: 0,
  loaded: 0,
  playedSeconds: 0,
  loadedSeconds: 0,
};

export default function useManim(user: string, topic: string) {
  const [state, setState] = useState<SectionList>({
    sections: [
      {
        title: "",
        id: "0",
        ready: true,
        video: "",
        question: {
          type: "mc",
          data: {
            question: "",
            choices: [],
            answer: -1,
          },
        },
        progressState: initialProgressState,
      },
    ],
    ready: false,
  });
  const numExplain = useRef(1);

  async function update(i: number, prompt: string, skip: boolean = true) {
    const name = "Explanation " + numExplain.current;
    const newState = {
      ready: true,
      sections: state.sections
        .slice(0, i)
        .concat([
          {
            ...state.sections[i],
            question: {
              ...state.sections[i].question,
              type: skip ? "skip" : state.sections[i].question.type,
            },
          },
        ])
        .concat([
          {
            // note: 2 explanations in a row won't work until videos are different
            title: name,
            ready: false,
            video: "",
            question: {
              type: "text",
              data: {
                question: "",
              },
            },
            progressState: initialProgressState,
          } as Section,
        ])
        .concat(state.sections.slice(i + 1)),
    };
    setState(newState);
    numExplain.current++;
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        setState({
          ready: true,
          sections: newState.sections.map((s) => {
            if (s.title === name)
              return {
                // note: 2 explanations in a row won't work until videos are different
                title: name,
                ready: true,
                video: "/LinearAlgebraOther.mp4",
                question: {
                  type: "text",
                  data: {
                    question: "Is this helpful?",
                  },
                },
                progressState: initialProgressState,
              } as Section;
            return s;
          }),
        });
        resolve(state.sections);
      }, 1000);
    });
  }

  function updateProgress(checkpoint: number, progressState) {
    setState((state) => ({
      sections: state.sections.map((s, i) => {
        if (i != checkpoint) return s;
        return { ...s, progressState: progressState };
      }),
      ready: state.ready,
    }));
  }

  function shuffleArray(array) {
    for (var i = array.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var temp = array[i];
      array[i] = array[j];
      array[j] = temp;
    }
  }

  const fetchSectionVideo = useCallback(
    async (id) => {
      const res = await fetchr("/api/video/" + id);
      if (res.headers.get("content-type") === "application/json") return false;
      const file = window.URL.createObjectURL(await res.blob());
      const { isReady, video } = {
        isReady: true,
        video: file,
      };
      console.log("ready", id);
      setState((state) => ({
        ...state,
        sections: state.sections.map((s) =>
          s.id === id
            ? {
                ...s,
                video: video,
                ready: isReady,
              }
            : s
        ),
      }));
      return isReady;
    },
    [setState]
  );

  const pingId = useCallback(
    (id: string) => {
      const interval = setInterval(async () => {
        if (await fetchSectionVideo(id)) clearInterval(interval);
      }, 2000);
      return () => clearInterval(interval);
    },
    [fetchSectionVideo]
  );

  useEffect(() => {
    if (user && topic) {
      // TODO: query api
      (async () => {
        const storyboards = await getStoryboards(user, topic);
        console.log(storyboards);
        const sections = storyboards.map((s, i) => {
          const sec: Section = {
            title: s.title,
            id: s.id,
            progressState: initialProgressState,
            video: "",
            ready: false,
            question: {
              type: "text",
              data: {
                question: "Is this helpful?",
              },
            },
          };

          // const sections = storyboards.map((s, i) => {
          //   const mc = i % 2 == 0; // alternate mc/fr
          //   const cs = s.data["multiple-choice-choices"].map((c, i) => ({
          //     correct: i == 0,
          //     choice: c,
          //   }));

          //   shuffleArray(cs);

          //   let answer = 0;
          //   for (let i = 1; i < cs.length; i++) if (cs[i].correct) answer = i;

          //   const sec: Partial<Section> = {
          //     title: s.title,
          //     id: s.id,
          //     progressState: initialProgressState,
          //     video: "",
          //     ready: false,
          //   };
          //   sec.question = mc
          //     ? {
          //         type: "mc",
          //         data: {
          //           question: s.data["multiple-choice-question"],
          //           choices: cs.map((c) => c.choice),
          //           answer: answer,
          //         },
          //       }
          //     : {
          //         type: "text",
          //         data: {
          //           question: s.data["free-response-question"],
          //         },
          //       };
          return sec as Section;
        });
        sections.forEach((s) => {
          pingId(s.id);
        });
        setState({ ready: true, sections: sections });

      })();

      // setTimeout(() => {
      //   setState({
      //     ready: true,
      //     sections: [
      //       {
      //         title: "Intro",
      //         progressState: {
      //           played: 0,
      //           loaded: 0,
      //           playedSeconds: 0,
      //           loadedSeconds: 0,
      //         },
      //         question: {
      //           type: "mc",
      //           data: QuizConfig,
      //         },
      //         video: "/LinearAlgebraIntro.mp4",
      //         ready: true,
      //       },
      //       {
      //         title: "Vectors",
      //         progressState: {
      //           played: 0,
      //           loaded: 0,
      //           playedSeconds: 0,
      //           loadedSeconds: 0,
      //         },
      //         question: {
      //           type: "text",
      //           data: {
      //             question:
      //               "Explain, in simple terms, the purpose of linear algebra.",
      //           },
      //         },
      //         video: "/LinearAlgebraIntroLarge.mp4",
      //         ready: true,
      //       },
      //       {
      //         title: "Matrices",
      //         progressState: {
      //           played: 0,
      //           loaded: 0,
      //           playedSeconds: 0,
      //           loadedSeconds: 0,
      //         },
      //         question: {
      //           type: "mc",
      //           data: QuizConfig,
      //         },
      //         video: "/LinearAlgebraIntro.mp4",
      //         ready: true,
      //       },
      //       {
      //         title: "Outro",
      //         progressState: {
      //           played: 0,
      //           loaded: 0,
      //           playedSeconds: 0,
      //           loadedSeconds: 0,
      //         },
      //         question: {
      //           type: "text",
      //           data: {
      //             question: "What do matrix multiplications conceptualize?",
      //           },
      //         },
      //         video: "/LinearAlgebraIntroLarge.mp4",
      //         ready: true,
      //       },
      //     ],
      //   });
      // }, 2000);
    }
  }, [user, topic, pingId]);

  return {
    ready: state.ready,
    data: state.sections,
    update: update,
    updateProgress: updateProgress,
  };
}
