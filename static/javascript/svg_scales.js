const width = 500,
    height = 400
    margin = {top: 20, right: 10, bottom: 20, left: 10};

const cardHeight = 60
    cardRadius = 5;

let svgHands = d3.select("div#hands").append("svg")
    // .attr("viewBox", [0, 0, width, height]);
    .attr("width", width)
    .attr("height", height);

let svgStack = d3.select("div#main").append("svg")
    .attr("width", width)
    .attr("height", 100);

let svgUseful = d3.select("div#useful").append("svg")
    .attr("width", width)
    .attr("height", height)
.append("g")
    .attr("class", "useful");

let svgUseless = d3.select("div#useless").append("svg")
    .attr("width", width)
    .attr("height", height)
.append("g")
    .attr("class", "useless");

// Scales for hands
let x = d3.scaleBand()
    .domain([0,1,2,3,4])  // [..."01234"].map(x => +x)
    .range([margin.left, width - margin.right])
    .padding(0.6);


let y = d3.scaleBand()
    .domain([0, 1])  // players.map(d => d.id)
    .range([margin.top, height - margin.bottom])
    .padding(0.6);

// Scales for the 5 colours (discarded stacks)
let xx = d3.scaleBand()
    .domain(["red", "blue", "green", "yellow", "white"])
    .range([margin.left, width - margin.right])
    .padding(0.6);

let yy = d3.scaleBand()
    .domain([1, 2, 3, 4, 5])  // nb_players
    .range([margin.top, height - margin.bottom])
    .padding(0.6);


// Handle drag and drop
let dragHandler = d3.drag()
    .on("start", function () {
        // Check if the card has transform attribute (translation)
        // if yes, use that as start of movement
        let current = d3.select(this);
        let transform = current.attr("transform");
        if (transform === null) {
            dx = current.attr("x") - d3.event.x;
            dy = current.attr("y") - d3.event.y;
        } else {
            let t = getTranslation(transform);
            dx = t[0] - d3.event.x;
            dy = t[1] - d3.event.y;
        }
    })
    .on("drag", function () {
        d3.select(this)
            .attr("transform", `translate(${d3.event.x + dx}, ${d3.event.y + dy})`);
    })
    .on("end", function () {
        let current = d3.select(this);
        let t = getTranslation(current.attr("transform"));
        current
            .attr("transform", `translate(${t[0]})`)  // default y = 0
        });
