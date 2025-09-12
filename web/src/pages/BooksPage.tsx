import { useEffect, useState } from "react";
import api from "../lib/api";

interface Author {
  id: number;
  name: string;
}

interface Genre {
  id: number;
  name: string;
}

interface Book {
  id: number;
  title: string;
  author_id: number | null;
  genre_id: number | null;
  year?: number;
  isbn?: string;
}

export default function BooksPage() {
  const [books, setBooks] = useState<Book[]>([]);
  const [authors, setAuthors] = useState<Author[]>([]);
  const [genres, setGenres] = useState<Genre[]>([]);

  // form state
  const [title, setTitle] = useState("");
  const [authorId, setAuthorId] = useState<number | "">("");
  const [genreId, setGenreId] = useState<number | "">("");
  const [year, setYear] = useState<number | "">("");
  const [isbn, setIsbn] = useState("");

  async function loadAll() {
    const [b, a, g] = await Promise.all([
      api.get<Book[]>("/books"),
      api.get<Author[]>("/authors"),
      api.get<Genre[]>("/genres"),
    ]);
    setBooks(b.data);
    setAuthors(a.data);
    setGenres(g.data);
  }

  async function addBook() {
    if (!title.trim()) return;
    await api.post("/books", {
      title,
      author_id: authorId || null,
      genre_id: genreId || null,
      year: year || null,
      isbn: isbn || null,
    });
    setTitle("");
    setAuthorId("");
    setGenreId("");
    setYear("");
    setIsbn("");
    loadAll();
  }

  async function deleteBook(id: number) {
    await api.delete(`/books/${id}`);
    loadAll();
  }

  useEffect(() => {
    loadAll();
  }, []);

  return (
    <div>
      <h2>Books</h2>

      <input
        value={title}
        placeholder="Book title"
        onChange={(e) => setTitle(e.target.value)}
      />

      <select
        value={authorId}
        onChange={(e) => setAuthorId(e.target.value ? Number(e.target.value) : "")}
      >
        <option value="">Select Author</option>
        {authors.map((a) => (
          <option key={a.id} value={a.id}>
            {a.name}
          </option>
        ))}
      </select>

      <select
        value={genreId}
        onChange={(e) => setGenreId(e.target.value ? Number(e.target.value) : "")}
      >
        <option value="">Select Genre</option>
        {genres.map((g) => (
          <option key={g.id} value={g.id}>
            {g.name}
          </option>
        ))}
      </select>

      <input
        type="number"
        value={year}
        placeholder="Year"
        onChange={(e) => setYear(e.target.value ? Number(e.target.value) : "")}
      />

      <input
        value={isbn}
        placeholder="ISBN"
        onChange={(e) => setIsbn(e.target.value)}
      />

      <button onClick={addBook}>Add</button>

      <ul>
        {books.map((b) => (
          <li key={b.id}>
            <strong>{b.title}</strong>
            {b.author_id &&
              ` by ${authors.find((a) => a.id === b.author_id)?.name ?? ""}`}
            {b.genre_id &&
              ` [${genres.find((g) => g.id === b.genre_id)?.name ?? ""}]`}
            {b.year && ` (${b.year})`}
            {b.isbn && ` – ${b.isbn}`}
            <button onClick={() => deleteBook(b.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
