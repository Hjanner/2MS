import { ref } from 'vue'

const searchTerm = ref('')

export function useSearchTerm () {
  const clearSearchTerm = () => searchTerm.value = ''

  return { searchTerm, clearSearchTerm }
}
