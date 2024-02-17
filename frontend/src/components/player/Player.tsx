import React from "react";
import ReactPlayer from "react-player/file";

export default function Player() {
  return (
    <div>
      <ReactPlayer playing controls={false} url="/LinearAlgebraIntro.mp4" />
    </div>
  );
}
