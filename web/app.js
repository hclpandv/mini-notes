
const form = document.querySelector("#note-form");
const titleInput = document.querySelector("#title");
const bodyInput = document.querySelector("#body");
const message = document.querySelector("#message");
const notesList = document.querySelector("#notes-list");

// Ask the Python server for the saved notes.
async function loadNotes() {
    try {
        const response = await fetch("/api/notes");

        if (!response.ok) {
            throw new Error("Could not load notes");
        }

        const data = await response.json();
        renderNotes(data.notes);
    } catch (error) {
        notesList.textContent = "Could not load notes. Please try again.";
    }
}

// Build the notes list using safe DOM methods.
function renderNotes(notes) {
    notesList.replaceChildren();

    if (notes.length === 0) {
        const empty = document.createElement("p");
        empty.className = "empty-state";
        empty.textContent = "No notes yet. Create your first one above!";
        notesList.append(empty);
        return;
    }

    for (const note of notes) {
        const card = document.createElement("article");
        card.className = "note";
        card.dataset.id = note.id;

        const title = document.createElement("h3");
        title.textContent = note.title;

        const body = document.createElement("p");
        body.textContent = note.body;

        const created = document.createElement("small");
        created.textContent = `Created: ${note.created_at}`;

        const deleteButton = document.createElement("button");
        deleteButton.type = "button";
        deleteButton.textContent = "Delete";

        deleteButton.addEventListener("click", () => {
            deleteNote(note.id);
        });

        card.append(title, body, created, deleteButton);
        notesList.append(card);
    }
}

// Send a new note to the Python server.
form.addEventListener("submit", async (event) => {
    event.preventDefault();

    message.textContent = "Saving...";

    try {
        const response = await fetch("/api/notes", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                title: titleInput.value,
                body: bodyInput.value
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Could not save note");
        }

        form.reset();
        message.textContent = "Note saved!";
        await loadNotes();
    } catch (error) {
        message.textContent = error.message;
    }
});

// Ask the Python server to delete a note.
async function deleteNote(id) {
    try {
        const response = await fetch(`/api/notes/${id}`, {
            method: "DELETE"
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Could not delete note");
        }

        message.textContent = "Note deleted.";
        await loadNotes();
    } catch (error) {
        message.textContent = error.message;
    }
}

// Load existing notes when the page opens.
loadNotes();
