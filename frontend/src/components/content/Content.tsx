import React from "react";
import { ScaleLoader } from "react-spinners";

export default function Content({ user, topic }) {
  return (
    <div className="w-full h-full justify-center items-center">
      <ScaleLoader loading color="#4EB389" />
    </div>
  );
}
