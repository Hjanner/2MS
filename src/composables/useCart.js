import { reactive } from 'vue'

export function useCart () {
  const cart = reactive({})

  const addItem = itemId => {
    if (!cart[itemId]) {
      cart[itemId] = { quantity: 1 }
    }
  }

  const removeItem = itemId => {
    if (cart[itemId]) {
      delete cart[itemId]
    }
  }

  const updateQuantity = (itemId, newQuantity) => {
    if (cart[itemId] && newQuantity > 0) {
      cart[itemId].quantity = newQuantity
    }
  }

  return { cart, addItem, removeItem, updateQuantity }
}
