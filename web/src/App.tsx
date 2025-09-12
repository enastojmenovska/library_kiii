import { useState } from "react";
import AuthorsPage from "./pages/AuthorsPage";
import GenresPage from "./pages/GenresPage";
import BooksPage from "./pages/BooksPage";

type Page = "authors" | "genres" | "books";

export default function App() {
  const [page, setPage] = useState<Page>("authors");

  return (
    <div className="container">
      <h1>Library App</h1>
      <nav style={{ marginBottom: "1rem" }}>
        <button onClick={() => setPage("authors")}>Authors</button>{" "}
        <button onClick={() => setPage("genres")}>Genres</button>{" "}
        <button onClick={() => setPage("books")}>Books</button>
      </nav>

      {page === "authors" && <AuthorsPage />}
      {page === "genres" && <GenresPage />}
      {page === "books" && <BooksPage />}
    </div>
  );
}
