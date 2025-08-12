<script setup>

</script>

<template>
  <v-container
    fluid
    class="bg-grey-lighten-3"
    height="100vh"
  >
    <v-col>
      <v-row>
        <v-btn to="/">Hola</v-btn>
      </v-row>
    </v-col>

    <v-col>
      <v-row>
        <v-list class="bg-transparent">
          <v-list-item
            class="bg-white mb-1"
            border="md"
            height="10vh"
            rounded
            slim
          >
            <template #title>
          <span class="">
            Tarjeta
          </span>
            </template>

            <template #prepend>
              <v-icon icon="mdi-credit-card"/>
            </template>

            <template #append>
              <v-icon
                color="primary"
                icon="mdi-minus-circle-outline"
              />
            </template>
          </v-list-item>

          <v-list-item
            class="bg-white"
            border="md"
            height="10vh"
            rounded
            slim
          >
            <template #title>
          <span class="">
            Tarjeta
          </span>
            </template>

            <template #prepend>
              <v-icon icon="mdi-credit-card"/>
            </template>

            <template #append>
              <v-icon
                color="primary"
                icon="mdi-minus-circle-outline"
              />
            </template>
          </v-list-item>

          <v-list-item
            class="bg-white"
            height="10vh"
            rounded
            slim
          >
            <template #title>
          <span class="">
            Añadir pago
          </span>
            </template>

            <template #append>
              <v-icon
                color="primary"
                icon="mdi-plus-circle-outline"
              />
            </template>
          </v-list-item>
        </v-list>
      </v-row>
    </v-col>
  </v-container>

  <OrderSummary />
</template>
