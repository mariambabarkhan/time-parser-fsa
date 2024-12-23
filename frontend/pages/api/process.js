export default async function handler(req, res) {
  if (req.method === "POST") {
    const { text } = req.body;
    try {
      const response = await fetch("http://127.0.0.1:5000/process", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text }),
      });
      const data = await response.json();
      res.status(200).json({ result: data.result });
    } catch (error) {
      res.status(500).json({ error: "Error connecting to backend" });
    }
  } else {
    res.status(405).json({ error: "Method not allowed" });
  }
}
