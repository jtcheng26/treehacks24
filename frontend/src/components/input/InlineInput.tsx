import React from "react";

export default function InlineInput({
  onSubmit = (str: string) => {},
  onChange = (str: string) => {},
  disabled = false,
  value = "",
}) {
  function handleChange(e) {
    onChange(e.target.value);
  }
  function handleSubmit(e) {
    if (e.key === "Enter") onSubmit(e.target.value);
  }
  return (
    <input
      className="text-primary bg-transparent outline-none placeholder-white"
      disabled={disabled}
      type="text"
      value={value}
      placeholder="__________"
      onChange={handleChange}
      onKeyDown={handleSubmit}
    ></input>
  );
}
