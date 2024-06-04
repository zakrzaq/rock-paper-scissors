<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useFetch, usePost } from "./api";
import { Status, Result } from "./interfaces";

const status = ref<Status | null>(null);
const player = ref<string | null>(null);
const result = ref<Result | null>(null);

const handleInputChange = (e: Event) => {
  const target = e.target as HTMLInputElement;
  player.value = target.value;
};

const submitPlayer = async () => {
  if (player.value) {
    usePost("/add_player", { player: player.value });
    const { data } = await useFetch("/status");
    status.value = data;
  }
};

const playGame = async (choice: string) => {
  const { data } = await usePost("/play", { choice });
  result.value = data;
};

const exitGame = async () => {
  usePost("/play", { choice: "exit" });
  const { data } = await useFetch("/status");
  status.value = data;
};

onMounted(async () => {
  const { data } = await useFetch("/status");
  status.value = data;
});
</script>

<template>
  <div>
    <h2>Rock - Paper - Scissors</h2>
    <div v-if="!!status && !status.player">
      <input
        type="text"
        name="player"
        id="player"
        placeholder="Enter your name..."
        @change="handleInputChange"
      />
      <button @click="submitPlayer">Submit</button>
    </div>

    <div v-if="!!status && status.player">
      <div>
        <p>Player score: {{ result?.player_score }}</p>
        <p>CPU score: {{ result?.cpu_score }}</p>
      </div>
      <div>
        <button @click="playGame('rock')">Rock</button>
        <button @click="playGame('paper')">Paper</button>
        <button @click="playGame('scissors')">Scissor</button>
      </div>
      <p v-if="!!result">
        You chose: {{ result.player_choice }} and CPU chose:
        {{ result.cpu_choice }}
      </p>
      <p v-if="!!result">Result: {{ result.result }}</p>
    </div>

    <div v-if="!!status && !!status.player">
      <button @click="exitGame">Exit</button>
    </div>
  </div>
</template>

<style scoped></style>
