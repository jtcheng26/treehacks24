import { QuizConfig } from "@/components/content/Content";
import { MCQuestionConfig } from "@/components/practice/MCQuizQuestion";
import { TextQuestionConfig } from "@/components/practice/TextQuizQuestion";
import { useEffect, useRef, useState } from "react";

/*
TODO: do the parentheses
Request all sections (show content once first ready)
set ready to true
when updating, insert new section (and re-render all after sections)
*/

export interface Section {
  title: string;
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
        ready: false,
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

  function update(i: number, prompt: string) {
    setState({
      ready: true,
      sections: state.sections
        .slice(0, i)
        .concat([
          {
            ...state.sections[i],
            question: { ...state.sections[i].question, type: "skip" },
          },
        ])
        .concat([
          { // note: 2 explanations in a row won't work until videos are different
            title: "Explanation " + numExplain.current,
            ready: true,
            video: "/LinearAlgebraOther.mp4",
            question: {
              type: "text",
              data: {
                question: "Is this helpful?",
              },
            },
            progressState: initialProgressState,
          } as Section,
        ])
        .concat(state.sections.slice(i + 1)),
    });
    numExplain.current++;
  }

  function updateProgress(checkpoint: number, progressState) {
    setState({
      sections: state.sections.map((s, i) => {
        if (i != checkpoint) return s;
        return { ...s, progressState: progressState };
      }),
      ready: state.ready,
    });
  }

  useEffect(() => {
    if (user && topic) {
      // TODO: query api
      setTimeout(() => {
        setState({
          ready: true,
          sections: [
            {
              title: "Intro",
              progressState: {
                played: 0,
                loaded: 0,
                playedSeconds: 0,
                loadedSeconds: 0,
              },
              question: {
                type: "mc",
                data: QuizConfig,
              },
              video: "/LinearAlgebraIntro.mp4",
              ready: true,
            },
            {
              title: "Vectors",
              progressState: {
                played: 0,
                loaded: 0,
                playedSeconds: 0,
                loadedSeconds: 0,
              },
              question: {
                type: "text",
                data: {
                  question:
                    "Explain, in simple terms, the purpose of linear algebra.",
                },
              },
              video: "/LinearAlgebraIntroLarge.mp4",
              ready: true,
            },
            {
              title: "Matrices",
              progressState: {
                played: 0,
                loaded: 0,
                playedSeconds: 0,
                loadedSeconds: 0,
              },
              question: {
                type: "mc",
                data: QuizConfig,
              },
              video: "/LinearAlgebraIntro.mp4",
              ready: true,
            },
            {
              title: "Outro",
              progressState: {
                played: 0,
                loaded: 0,
                playedSeconds: 0,
                loadedSeconds: 0,
              },
              question: {
                type: "text",
                data: {
                  question: "What do matrix multiplications conceptualize?",
                },
              },
              video: "/LinearAlgebraIntroLarge.mp4",
              ready: true,
            },
          ],
        });
      }, 2000);
    }
  }, [user, topic]);

  return {
    ready: state.ready,
    data: state.sections,
    update: update,
    updateProgress: updateProgress,
  };
}
