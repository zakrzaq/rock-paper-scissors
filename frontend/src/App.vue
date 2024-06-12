<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import { useFetch, usePost } from "./api";
import { Status, Result } from "./interfaces";

import Trophy from './assets/trophy.png'
import Cross from './assets/cross.png'
import Cpu from './assets/cpu.png'
import User from './assets/user.png'
import Rock from './assets/rock.png'
import Paper from './assets/paper.png'
import Scissors from './assets/scissors.png'

const status = ref<Status | null>(null);
const player = ref<string | null>(null);
const result = ref<Result | null>(null);
const resultValue = ref<string | null>();
const cpuChoice = ref<string | null>();
const playerChoice = ref<string | null>();

const resultIcon = computed(() => {
  if (resultValue.value == 'player_win') return Trophy
  if (resultValue.value == 'cpu_win') return Cpu
  return Cross
})
const cpuChoiceIcon = computed(() => {
  if (result.value?.cpu_choice === 'rock') return Rock
  if (result.value?.cpu_choice === 'paper') return Paper
  return Scissors
});
const playerChoiceIcon = computed(() => {
  if (result.value?.player_choice === 'rock') return Rock
  if (result.value?.player_choice === 'paper') return Paper
  return Scissors
});

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
  resultValue.value = result.value?.result
  cpuChoice.value = result.value?.cpu_choice
  playerChoice.value = result.value?.player_choice
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
      <div class="actions">
        <button @click="playGame('rock')" class="btn-icon">
          <img :src="Rock" class="icon" />
        </button>
        <button @click="playGame('paper')" class="btn-icon">
          <img :src="Paper" class="icon" />
        </button>
        <button @click="playGame('scissors')" class="btn-icon">
          <img :src="Scissors" class="icon" />
        </button>
      </div>

      <img v-if="resultValue" :src="resultIcon" alt="result icon" class="icon" />

      <div v-if="!!result" class="stats">
        <p><img :src="User" alt="user avatar" class="icon--small"></p>
        <p><img :src="Cpu" alt="cpu avatar" class="icon--small"></p>
        <p>{{ result?.player_score }}</p>
        <p>{{ result?.cpu_score }}</p>
        <p><img :src="playerChoiceIcon" alt="" class="icon--small" /></p>
        <p><img :src="cpuChoiceIcon" alt="" class="icon--small" /></p>
      </div>

    </div>

    <div v-if="!!status && !!status.player">
      <button @click="exitGame">Exit</button>
    </div>
  </div>
</template>

<style scoped>
.stats {
  display: grid;
  grid-template: repeat(3, 1fr) / repeat(2, 200px);
}

.actions {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-bottom: 25px;
}

.btn-icon {
  min-width: 90px;
  min-height: 75px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.icon {
  max-width: 50px;
  height: auto;
}

.icon--small {
  max-width: 25px;
  height: auto;
}
</style>
