<script>
    // No JS here for now buddy
    //Sike

    let targetUrl = $state(""); // finally some runes baby

    let shrinkedUrl = $state(""); // to hold the short URL from the backend

    // commented the former url out cause i was running two projects and needed to use port 8001
    // even in the back cors i had to add both 5173 and 5174 for svelte
    //let urlBase = $state("http://localhost:8000");
    // for now it'll aways point to localhost, since it's locally scoped
    // so much for shortening ig, but if i do scale, i can then point to an api_url in an env file
 
    const urlBase = import.meta.env.VITE_API_URL || "http://localhost:8001";

    async function shrinkUrl() {
        // sending a POST request to FastAPI
        const response = await fetch(`${urlBase}/url`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ target_url: targetUrl }),
        }); // to match with @app.post("/url") in FastAPI, the pydantic model

        if (response.ok) {
            const data = await response.json(); // to take the JSON object from FastAPI and turn it into a JavaScript object
            // then updating our state variable with the new short code
            shrinkedUrl = `${urlBase}/${data.your_new_short_url}`;
        } else {
            alert(
                "I think you put a bad URL blud, because something went wrong",
            );
        }

        targetUrl = ""; // just setting it to empty to clear the input
    }
</script>

<main
    class="min-h-screen bg-slate-950 flex items-center justify-center p-4 font-sans"
>
    <div
        class="bg-slate-800 border border-slate-800 rounded-lg p-8 w-full max-w-lg shadow-2x1"
    >
        <h1 class="text-2x1 font-semibold text-slate100 mb-2">
            Ayz URL Shortener
        </h1>
        <p class="text-slate-400 mb-6">
            Don't believe or understand the title, then paste a long ahh URL and
            see
        </p>

        <div class="flex flex-col sm:flex-row gap-3">
            <input
                type="text"
                placeholder="Paste that URL here"
                bind:value={targetUrl}
                class="flex-1 bg-slate-950 border border-slate-700 text-slate-200 text-sm rounded-md px-4 py-3 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-colors"
            />
            <button
                type="submit"
                onclick={shrinkUrl}
                class="bg-emerald-500 hover:bg-emerald-600 text-white font-semibold py-3 px-6 rounded-md transition-colors"
            >
                Shrink It
            </button>
        </div>
        <!--To show that bind:value happens real time-->
        <p class="text-xs text-slate-500 mt-4">
            You're literally typing: {targetUrl}
        </p>

        {#if shrinkedUrl}
            <div
                class="mt-6 p-4 bg-emerald-950 border border-emerald-900 rounded-md"
            >
                <span
                    class="block text-emerald-500 text-xs font-bold uppercase tracking-wider mb-1"
                    >Nice one bro! Your short link is...</span
                >
                <a
                    href={shrinkedUrl}
                    target="_blank"
                    class="text-emerald-100 hover:text-white hover:underline truncate block"
                    >{shrinkedUrl}</a
                >
                <!--Used anchor tag to make it clickable-->
            </div>
        {/if}
    </div>
</main>

<!-- <style>

    /* To learn tailwind, i decided to poof this custom styles block*/

    /*Global Dark Mode Setup */
    :global(body) {
        background-color: #0a1118;
        color: #e6f4f8;
        font-family: "Poppins", sans-serif;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        margin: 0;
    }

    .start_container {
        width: 100%;
        max-width: 540px;
        padding: 24px;
    }

    .start_card {
        background-color: #121e2a;
        border-radius: 16px;
        padding: 40px;
        box-shadow: 0 2px 6px #1b2a3a;
        text-align: center;
    }

    h1 {
        margin-top: 0;
        color: #00f5d4;
    }
    p {
        color: #7fa2b7;
        margin-bottom: 24px;
    }

    .input_wrapper {
        display: flex;
        gap: 8px;
    }

    input {
        flex: 1;
        padding: 12px 16px;
        border: 1px solid #1b2a3a;
        border-radius: 8px;
        background: #121e2a;
        font-size: 1rem;
        outline: none;
    }

    input:focus {
        border-color: #00f5d4;
    }

    button {
        padding: 12px 24px;
        font-weight: bold;
        cursor: pointer;
        transition:
            transform 0.1s,
            filter 0.2s;
        border: none;
        border-radius: 8px;
        background-color: #121e2a;
        color: #7fa2b7;
    }

    button:hover {
        filter: brightness(1.2);
        color: #e6f4f8;
        background-color: #00bac5;
    }
    button:active {
        transform: scale(0.94);
        background-color: #00bac5;
    }
</style> -->
