// altocumulus
// https://stackoverflow.com/questions/38224875/replacing-d3-transform-in-d3-v4
function getTranslation(transform) {
    // Create a dummy g for calculation purposes only. This will never
    // be appended to the DOM and will be discarded once this function
    // returns.
    var g = document.createElementNS("http://www.w3.org/2000/svg", "g");

    // Set the transform attribute to the provided string value.
    g.setAttributeNS(null, "transform", transform);

    // consolidate the SVGTransformList containing all transformations
    // to a single SVGTransform of type SVG_TRANSFORM_MATRIX and get
    // its SVGMatrix.
    var matrix = g.transform.baseVal.consolidate().matrix;

    // As per definition values e and f are the ones for the translation.
    return [matrix.e, matrix.f];
}

function drawHand(player) {
    let g = svgHands.append("g").attr("id", "player"+player.id);

    let card = g.selectAll(".card")
        .data(player.hand)
        .enter()
        .append("g")
        .attr("player", player.id)
        .attr("class", "card");

    card.append("rect")
        .attr("x", (_, i) => x(i))
        .attr("y", y(player.id))
        .attr("width", x.bandwidth())
        .attr("height", cardHeight)
        .attr("rx", cardRadius);
        // .class?

    card.append("text")
        .attr("x", (_, i) => x(i) + x.bandwidth()/2)
        .attr("y", y(player.id) + cardHeight/2)
        .attr("dy", "0.4em")
        .text(d => d.number)
        .style("fill", d => d.colour);
        // .attr("class", "card-text");
}

function drawPlayed(played) {
    let g = svgStack.append("g")//.attr("class", "main");

    let card = g.selectAll(".card")
        .data(played)
        .enter()
        .append("g")
        .attr("class", "card");

    card.append("rect")
        .attr("x", d => xx(d.colour))
        .attr("y", margin.top)
        .attr("width", xx.bandwidth())
        .attr("height", cardHeight)
        .attr("rx", cardRadius);

    card.append("text")
        .attr("x", d => xx(d.colour) + xx.bandwidth()/2)
        .attr("y", margin.top + cardHeight/2)
        .attr("dy", "0.4em")
        .text(d => d.number)
        .style("fill", d => d.colour);
        // .attr("class", "card-text");
}

function drawDiscarded(g, played) {
    let card = g.selectAll(".card")
        .data(played)
        .enter()
        .append("g")
        .attr("class", "card");

    card.append("rect")
        .attr("x", d => xx(d.colour))
        .attr("y", d => yy(d.number))
        .attr("width", xx.bandwidth())
        .attr("height", cardHeight)
        .attr("rx", cardRadius)

    card.append("text")
        .attr("x", d => xx(d.colour) + xx.bandwidth()/2)
        .attr("y", d => yy(d.number) + cardHeight/2)
        .attr("dy", "0.4em")
        .text(d => d.number)
        .style("fill", d => d.colour);
        // .attr("class", "card-text");
}

function drawBoard(data) {
    // Draw cards
    let players = data.players;

    players.forEach(d => drawHand(d));
    svgHands.select("#player0") // Set the current player as invisible
        .selectAll(".card")
        .attr("class", "card-invisible");
    dragHandler(svgHands.selectAll(".card-invisible"));
    // TODO: change to play functions

    drawPlayed(data.stacks.played);
    drawDiscarded(svgUseful, data.stacks.discardedUseful);
    drawDiscarded(svgUseless, data.stacks.discardedUseless);
}

function updateHeader(data) {
    $("#current").text(data.current_id);
    $("#lifes").text(data.lifes);
    $("#clues").text(data.clues);
    $("#remaining").text(data.remaining);
}

function emitPlayed(socket, action, player_id, card_id) {
    if (action === "play" || action === "discard") {
        // var for function scope instead of let
        var object = {
            data : {
                id : player_id,
                action : action,
                args : {card_id : card_id}
            }
        };
    } else if (action === "hint") {
        var object = {};
    }

    socket.emit('played', object);
}
