const width = 500
    height = 400
    margin = {top: 20, right: 10, bottom: 20, left: 10}
    btnMargin = {top: 20, right: 30, bottom: 20, left: 30};

const cardHeight = 60
    cardRadius = 5;

const btnHeight = height
    btnWidth = 50;

// The player hands
let svgHands = d3.select("div#hands").append("svg")
    // .attr("viewBox", [0, 0, width, height]);
    .attr("width", width)
    .attr("height", height);

// Discard button
let btnDiscard = svgHands.append("rect")
    .attr("x", 0)
    .attr("y", 0)
    .attr("width", btnWidth)
    .attr("height", btnHeight)
    .attr("id", "discard");

let coordsDiscard = [
    [0,0], [btnWidth, 0], [btnWidth, btnHeight], [0, btnHeight]
];

svgHands.append("text")
    .attr("x", 0)
    .attr("y", btnHeight / 2)
    .attr("text-anchor", "middle")
    .attr("dx", 30)
    .text("Discard")
    .attr("class", "vertical-left");

let coordsPlay = [
    [width - btnWidth, 0], [width, 0], [width, btnHeight], [width - btnWidth, btnHeight]
];

// Play button
let btnPlay = svgHands.append("rect")
    .attr("x", width - btnWidth)
    .attr("y", 0)
    .attr("width", btnWidth)
    .attr("height", btnHeight)
    .attr("id", "play");

svgHands.append("text")
    .attr("x", width - btnWidth)
    .attr("y", btnHeight / 2)
    .attr("text-anchor", "middle")
    .attr("dx", btnWidth / 2)
    .text("Play")
    .attr("class", "vertical-right")


// The other stacks
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
    .range([btnMargin.left, width - btnMargin.right])
    .padding(0.6);


let y = d3.scaleBand()
    .domain([0, 1])  // players.map(d => d.id)
    .range([btnMargin.top, height - btnMargin.bottom])
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
            dx = - d3.event.x;
            dy = - d3.event.y;
        } else {
            let t = getTranslation(transform);
            dx = t[0] - d3.event.x;
            dy = t[1] - d3.event.y;
        }
    })
    .on("drag", function () {
        d3.select(this)
            .attr("transform", `translate(${d3.event.x + dx}, ${d3.event.y + dy})`);
    });

function setUpDragHandlerOnEnd(dragHandler, socket) {
    dragHandler.on("end", function () {
        let current = d3.select(this);
        let player_id = current.attr("player");
        let data = current.node().__data__;
        let card_id = data.id;

        let t = getTranslation(current.attr("transform"));
        let pos = [+current.select("rect").attr("x") + t[0] + 15,  // +15 compensates width of card
                   +current.select("rect").attr("y") + t[1]];

        if (d3.polygonContains(coordsPlay, pos)) {
            console.log("Play!")
            console.log(data.colour + "-" + data.number.toString() + " id: " + data.id)
            emitPlayed(socket, "play", player_id, card_id)
        } else if (d3.polygonContains(coordsDiscard, pos)) {
            console.log("Discard!")
            console.log(data.colour + "-" + data.number.toString() + " id: " + data.id)
            emitPlayed(socket, "discard", player_id, card_id)
        }

        current
            .attr("transform", `translate(${t[0]})`)  // default y = 0
        });
}
