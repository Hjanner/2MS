import { computed, reactive, readonly } from 'vue'

const cart = reactive({})

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

export function useCart () {
  const getCart = () => readonly(cart)

  const clearCart = () => {
    for (const key in cart) {
      delete cart[key]
    }
  }

  const addItem = (itemId, itemPrice) => {
    if (!cart[itemId]) {
      cart[itemId] = { price: itemPrice, quantity: 1 }
    }
  }

  const removeItem = itemId => {
    if (cart[itemId]) {
      delete cart[itemId]
    }
  }

  const createItemQuantityModel = itemId => {
    return computed({
      get: () => getItemQuantity(itemId),
      set: newQuantity => setItemQuantity(itemId, newQuantity),
    })
  }

  const getItemSubtotal = itemId => cart[itemId].price * cart[itemId].quantity

  const getTotalPrice = () => {
    let total = 0

    for (const key in cart) {
      total += cart[key].price * cart[key].quantity
    }

    return total
  }

  return {
    getCart,
    clearCart,
    addItem,
    removeItem,
    createItemQuantityModel,
    getItemSubtotal,
    getTotalPrice,
  }
}
