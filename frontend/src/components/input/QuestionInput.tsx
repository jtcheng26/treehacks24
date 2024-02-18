import React, { useRef } from "react";

export default function QuestionInput({
  onSubmit = (str: string, callback: () => void) => {},
  onFocus = () => {},
  onUnfocus = () => {},
  visible = true,
  placeholder = "I have a question...",
  maxWidth = "500px",
}) {
  const inputRef = useRef(null);
  function handleSubmit(e) {
    if (e.key === "Enter")
      onSubmit(e.target.value, () => {
        if (inputRef) {
          inputRef.current.value = "";
          inputRef.current.blur();
        }
      });
  }
  function handleFocus(e) {
    onFocus();
  }
  function handleUnfocus(e) {
    onUnfocus();
  }
  return (
    <input
      className="bg-slate-800 h-12 px-4 text-sm outline-none rounded-lg outline-0 focus:outline-2 outline-slate-600 transition-all duration-200"
      style={{ width: visible ? maxWidth : 0, opacity: visible ? 1 : 0 }}
      type="text"
      placeholder={placeholder}
      onKeyDown={handleSubmit}
      onFocus={handleFocus}
      onBlur={handleUnfocus}
      ref={inputRef}
    ></input>
  );
}
