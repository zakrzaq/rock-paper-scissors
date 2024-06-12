export interface Status {
  cpu_score: number;
  is_active: boolean;
  player: string | null;
  player_score: number;
}

export interface Result {
  cpu_choice: string;
  cpu_score: number;
  player_choice: string;
  player_score: number;
  result: string;
}
