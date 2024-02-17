import React from "react";
import { ScaleLoader } from "react-spinners";
import useManim from "../../hooks/useManim";
import Player from "../player/Player";
import ReplayButton from "../button/ReplayButton";
import QuestionInput from "../input/QuestionInput";

export default function Content({ user, topic }) {
  const { ready, data, update } = useManim(user, topic);
  const loading = !ready;
  return (
    <div className="w-full h-full flex flex-col">
      <ScaleLoader loading={loading} color="#4EB389" />
      {!loading ? (
        <>
          <div className="w-full flex justify-center items-center pt-10">
            <Player />
          </div>
          <div className="w-full flex-row items-center justify-center">
            <ReplayButton />
            <QuestionInput />
          </div>
          <div></div>
        </>
      ) : (
        ""
      )}
    </div>
  );
}
