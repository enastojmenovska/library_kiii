import { useEffect, useState } from "react";
import api from "../lib/api";

interface Genre {
  id: number;
  name: string;
}

export default function GenresPage() {
  const [genres, setGenres] = useState<Genre[]>([]);
  const [newName, setNewName] = useState("");

  async function loadGenres() {
    const res = await api.get<Genre[]>("/genres");
    setGenres(res.data);
  }

  async function addGenre() {
    if (!newName.trim()) return;
    await api.post("/genres", { name: newName });
    setNewName("");
    loadGenres();
  }

  async function deleteGenre(id: number) {
    await api.delete(`/genres/${id}`);
    loadGenres();
  }

  useEffect(() => {
    loadGenres();
  }, []);

  return (
    <div>
      <h2>Genres</h2>
      <input
        value={newName}
        placeholder="Genre name"
        onChange={(e) => setNewName(e.target.value)}
      />
      <button onClick={addGenre}>Add</button>
      <ul>
        {genres.map((g) => (
          <li key={g.id}>
            {g.name}{" "}
            <button onClick={() => deleteGenre(g.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
