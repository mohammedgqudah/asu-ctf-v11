document.addEventListener("DOMContentLoaded", function(event) {
	let default_items = [
		{
			title: 'Write a challenge',
			done: false,
		},
		{
			title: 'Do something important',
			done: true,
		},
		{
			title: 'Do something less important',
			done: true,
		},
		{
			title: "I don't really have to do this",
			done: false,
		}
	]

	let db = []

	const urlObj = new URL(window.location.href);
	const shared_items = urlObj.searchParams.get("items");
	if (shared_items) {
		db = JSON.parse(atob(shared_items));
	} else {
		db = default_items;
	}
	updateSharedLink();

	// Scripts? Check
	// Iframes? Check
	// onload/onerror attributes? Check!!
	function safe(text) {
		return text
			.replace(/on\w+\s*=/g, 'safe_attr')
			.replace(/<script/ig, "")
			.replace(/iframe/ig, '')
	}

	let todosContainer = document.getElementById('todos');

	db.map(todo => {
		let element = document.createElement('div');
		element.classList.add("todo");
		element.innerHTML = safe(todo.title)
		if (todo.done) {
			element.classList.add('done')
		}
		return element;
	}).forEach(h3 => {
		todosContainer.appendChild(h3)
	});

	const form = document.querySelector('form');

	// Add a new TODO item.
	form.addEventListener('submit', function(event) {
		event.preventDefault();

		const input = form.querySelector('input[type="text"]');
		const item = input.value;
		if (item) {
			let element = document.createElement('div');
			// Make sure the item is safe to render in HTML :D
			element.innerHTML = safe(item)
			todosContainer.appendChild(element)
			db.push({ title: item, done: false })
			updateSharedLink();
		}

		form.reset();
	});

	function updateSharedLink() {
		let serialized = JSON.stringify(db);
		let payload = encodeURIComponent(btoa(serialized));
		let link = window.location.origin + `?items=${payload}`
		document.getElementById('share').value = link;
	}
});

function add(e) {
	e.preventDefault();
	e.target.reset();
}
