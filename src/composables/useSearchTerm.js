import { ref } from 'vue'

const searchTerm = ref('')

export function useSearchTerm () {
  const matchesSearchTerm = string => string.toLowerCase().includes(searchTerm.value.toLowerCase())

  const clearSearchTerm = () => searchTerm.value = ''

  return { searchTerm, matchesSearchTerm, clearSearchTerm }
}
