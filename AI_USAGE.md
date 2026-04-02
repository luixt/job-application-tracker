# AI Usage Documentation

## Tools Used
- Gemini (Gemini 3 Flash): primary used for architectural logic, debugger, and CSS styling.

## Key Prompts
1. "Why should we put SQL in the routes? Isn't better to include all of that inside the database.py instead of the app.py?"

2. "How do I make the HTML change based on what I’m doing? Like, show an 'Edit' title instead of 'Add' in the same box?"

3. "The LinkedIn link of contacts should be on the name, the phone needs to be under the email, and how can I include a whole new column for Notes."

4. "How do I store a list of skills in one database cell and then check if I have those skills later?"

## What Worked Well
### The AI effectively pivoted to:

- Jinja2 Logic: Using {% if %}, {% for %}, and {% end %} was a game-changer. It allowed me to loop through the database to build tables automatically and toggle the "Edit" form on and off without making a bunch of separate pages.

- Separation of Concerns: Moving all the "Data Logic" (SQL) into database.py and leaving app.py to just handle the "Traffic" (Routing) made the project much more professional.

- The Matcher: The intersection of Python sets to calculate a percentage based on JSON data from MySQL worked way better than I expected.

## What I Modified
- I didn't let the AI settle for basic tables. I insisted on grouping data (like City/State or Title/Company) to keep the layout from getting cluttered.

- I had the AI create specific classes like btn-cancel and edit-highlight because the default browser links and colors were pretty ugly.

- I added required tags to the forms and onclick="confirm()" to the delete buttons so I wouldn't accidentally wipe out my data.

- I had to ask for a custom Flask filter (from_json) because the AI forgot that Flask doesn't natively know how to read a JSON string inside a template.

## Lessons Learned
- HTML isn't just text. Learning that I could use "logic" ({% if %}) inside HTML to change colors or hide buttons was probably the most important thing I learned. It’s what makes it an "App" and not just a "Site."

- Don't Repeat Code. Using a base.html and "extending" it meant I only had to fix the navbar once instead of five times.

- AI is great at boilerplate, but it doesn't have "taste." You have to keep pushing it to get the alignment, colors, and layout exactly where you want them.

- I learned how FOREIGN KEY constraints actually work in practice—like how deleting a company can automatically clean up its jobs. It’s a lot more powerful than I realized.