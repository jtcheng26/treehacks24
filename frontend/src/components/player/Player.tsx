import React from "react";
import ReactPlayer from "react-player/file";

export default function Player({
  url,
  playing = true,
  playerRef = null,
  onProgress = ({ played, loaded, playedSeconds, loadedSeconds }) => {},
}) {
  return (
    <div className="flex-grow flex justify-center items-center">
      <ReactPlayer
        onProgress={onProgress}
        playing={playing}
        controls={false}
        url={url}
        ref={playerRef}
      />
    </div>
  );
}
