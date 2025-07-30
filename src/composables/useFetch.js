import { ref } from 'vue'

export function useFetch (url) {
  const data = ref(null)
  const error = ref(null)

  fetch(url)
    .then(res => res.json())
    .then(json => (data.value = json))
    .catch(error_ => (error.value = error_))

  return { data, error }
}
