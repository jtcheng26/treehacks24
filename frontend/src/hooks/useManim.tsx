import { useEffect, useState } from "react";

export default function useManim(user: string, topic: string) {
  const [state, setState] = useState({
    ready: false,
    data: null,
  });

  function update(prompt: string) {}

  useEffect(() => {
    if (user && topic) {
      // TODO: query api
      setTimeout(() => {
        setState({ ready: true, data: {} });
      }, 2000)
     
    }
  }, [user, topic]);

  return { ready: state.ready, data: state.data, update: update };
}
