import bodyParser from 'body-parser'
import express from 'express'

const app = express();
const port = 5002;

app.use(bodyParser.urlencoded({ extended: false }));
app.set('view engine', 'pug');
app.use(express.static('public'))

let notes = []

app.get('/', (req, res) => {
	res.render('index', { title: 'Baby XSS'})
});

app.listen(port, () => {
	console.log(`Server is running on http://localhost:${port}`);
});
