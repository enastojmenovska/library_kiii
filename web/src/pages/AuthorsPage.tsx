import { useEffect, useState } from "react";
import api from "../lib/api";

interface Author {
  id: number;
  name: string;
}

export default function AuthorsPage() {
  const [authors, setAuthors] = useState<Author[]>([]);
  const [newName, setNewName] = useState("");

  async function loadAuthors() {
    const res = await api.get<Author[]>("/authors");
    setAuthors(res.data);
  }

  async function addAuthor() {
    if (!newName.trim()) return;
    await api.post("/authors", { name: newName });
    setNewName("");
    loadAuthors();
  }

  async function deleteAuthor(id: number) {
    await api.delete(`/authors/${id}`);
    loadAuthors();
  }

  useEffect(() => {
    loadAuthors();
  }, []);

  return (
    <div>
      <h2>Authors</h2>
      <input
        value={newName}
        placeholder="Author name"
        onChange={(e) => setNewName(e.target.value)}
      />
      <button onClick={addAuthor}>Add</button>
      <ul>
        {authors.map((a) => (
          <li key={a.id}>
            {a.name}{" "}
            <button onClick={() => deleteAuthor(a.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
