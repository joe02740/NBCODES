const fetchAIExplanation = async (query, context) => {
  try {
    const response = await fetch(`${process.env.REACT_APP_API_URL}/ai_explain`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query, context }),
    });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    return data.explanation;
  } catch (error) {
    console.error("Error fetching AI explanation:", error);
    return "Unable to fetch explanation at this time.";
  }
};