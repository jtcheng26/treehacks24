export async function postQuestionAnswer(question: string, answer: string) {
  return fetchr("/api/text_answer", {
    method: "POST",
    body: JSON.stringify({
      question: question,
      answer: answer,
    }),
  });
}

function serialize(obj) {
  var str = [];
  for (var p in obj)
    if (obj.hasOwnProperty(p)) {
      str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
    }
  return str.join("&");
}

export async function getStoryboards(audience: string, concept: string) {
  return await (
    await fetchr(
      `/api/init/?${serialize({ audience: audience, concept: concept })}`
    )
  ).json();
}

export async function fetchr(route: string, params = {}) {
  return fetch(process.env.NEXT_PUBLIC_BASE_URL + route, params);
}
