import React from "react";

export default function QuestionInput({
  onSubmit = (str: string) => {},
  onFocus = () => {},
  onUnfocus = () => {},
  visible = true,
}) {
  function handleSubmit(e) {
    if (e.key === "Enter") onSubmit(e.target.value);
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
      style={{ width: visible ? 500 : 0, opacity: visible ? 1 : 0 }}
      type="text"
      placeholder="I have a question..."
      onKeyDown={handleSubmit}
      onFocus={handleFocus}
      onBlur={handleUnfocus}
    ></input>
  );
}
