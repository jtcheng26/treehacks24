import React, { useEffect } from "react";

export default function Skip({ callback, visible }) {
  useEffect(() => {
    if (visible) callback();
  }, [visible, callback]);
  return <div></div>;
}
