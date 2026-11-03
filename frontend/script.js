document.getElementById('bidForm').addEventListener('submit', async function(e) {
    e.preventDefault(); // Stop the browser's default process of handling form submission behaviour.

    // Gather values from input fields
    const payload = {
        client_budget_inr: parseFloat(document.getElementById('client_budget_inr').value),
        client_avg_spend_inr: parseFloat(document.getElementById('client_avg_spend_inr').value),

        // Here we use parseInt() instead of parseFloat() because reviews are whole numbers..
        client_total_reviews: parseInt(document.getElementById('client_total_reviews').value),

        freelancer_experience_yrs: parseInt(document.getElementById('freelancer_experience_yrs').value),
        freelancer_rating: parseFloat(document.getElementById('freelancer_rating').value),
        proposal_count: parseInt(document.getElementById('proposal_count').value),
        skill_match_score: parseFloat(document.getElementById('skill_match_score').value),
        freelancer_bid_inr: parseFloat(document.getElementById('freelancer_bid_inr').value)
    };

    try {
        // Send POST request to FastAPI backend
        const response = await fetch('https://freelancebidder-production.up.railway.app', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload) // Converts JavaScript object into JSON string before sending
        });

        if (!response.ok) {
            throw new Error('Failed to connect to the prediction server.');
        }

        const data = await response.json(); // Converts received JSON response into a JavaScript object

        // Hide placeholder and show results card
        document.getElementById('placeholderResult').classList.add('hidden');
        document.getElementById('resultCard').classList.remove('hidden');

        // Update Win Probability display
        const winProbElem = document.getElementById('winProbValue');
        const badgeElem = document.getElementById('badgeStatus');
        const prob = data.win_probability_percent; // we get this probability percentage from the backendAPI
        
        winProbElem.innerText = `${prob}%`;

        // Style badge based on win probability
        if (prob >= 50) {
            winProbElem.className = "text-4xl font-black mt-2 text-emerald-400";
            badgeElem.className = "inline-block mt-3 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-500/20 text-emerald-300";
            badgeElem.innerText = "🟢 High Winning Chance";
        } else if (prob >= 25) {
            winProbElem.className = "text-4xl font-black mt-2 text-amber-400";
            badgeElem.className = "inline-block mt-3 px-3 py-1 rounded-full text-xs font-semibold bg-amber-500/20 text-amber-300";
            badgeElem.innerText = "🟡 Moderate Chance";
        } else {
            winProbElem.className = "text-4xl font-black mt-2 text-rose-400";
            badgeElem.className = "inline-block mt-3 px-3 py-1 rounded-full text-xs font-semibold bg-rose-500/20 text-rose-300";
            badgeElem.innerText = "🔴 Low Chance";
        }

        // Update Ratio
        document.getElementById('ratioValue').innerText = data.bid_to_budget_ratio;

        // Populate Insights List
        const insightsList = document.getElementById('insightsList');
        insightsList.innerHTML = ''; // we clear the list before inserting new insights.
        data.insights.forEach(insight => {
            const li = document.createElement('li'); // Creates a new HTML list item <li> represents an individual list item.
            li.innerHTML = `• ${insight}`;
            insightsList.appendChild(li); // Adds the newly created child list item inside the unordered list.
        });

    } catch (error) {
        alert('Error connecting to backend API. Ensure your FastAPI server is running with uvicorn!');
        console.error(error);
    }
});
