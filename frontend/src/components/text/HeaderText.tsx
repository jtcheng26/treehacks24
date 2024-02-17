import React from "react";

export default function HeaderText({ children, shrink = false }) {
  return (
    <h1
      className={"font-bold text-3xl " + (shrink ? "opacity-40" : "")}
    >
      {children}
    </h1>
  );
}
