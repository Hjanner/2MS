import { ref } from 'vue'

const payments = ref([])

export function usePayments () {
    const setPayment = (paymentId, paymentMethod, paymentAmount) => {
        payments.value.push({ id: paymentId, method: paymentMethod, amount: paymentAmount })
    }

    const removePayment = paymentId => delete payments[paymentId]

    return { setPayment, removePayment }
}