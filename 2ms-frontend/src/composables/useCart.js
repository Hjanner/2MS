import { computed, reactive, readonly } from 'vue'

const cart = reactive({})

export function useCart () {
  const getCart = () => readonly(cart)

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

  const getItemQuantity = itemId => {
    if (cart[itemId]) {
      return cart[itemId].quantity
    }
  }

  const setItemQuantity = (itemId, newQuantity) => {
    if (cart[itemId] && newQuantity > 0) {
      cart[itemId].quantity = newQuantity
    }
  }

  const createItemQuantityModel = itemId => {
    return computed({
      get: () => getItemQuantity(itemId),
      set: newQuantity => setItemQuantity(itemId, newQuantity),
    })
  }

  return {
    getCart,
    addItem,
    removeItem,
    getItemQuantity,
    setItemQuantity,
    createItemQuantityModel,
  }
}
