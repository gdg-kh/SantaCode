function getRabbitRow(type, outerFace, innerFace) {
    // type: 0=feet, 1=face, 2=ears, -1=empty
    const empty = '       ';
    if (type === -1) return empty + empty;

    const rFeet = ' (> <) ';
    const rEars = ' (\\_/) ';

    let part1 = empty;
    let part2 = empty;

    if (type === 0) { part1 = rFeet; part2 = rFeet; }
    if (type === 1) { part1 = outerFace; part2 = innerFace; }
    if (type === 2) { part1 = rEars; part2 = rEars; }

    return part1 + part2;
}


function getGiftRow(type, side) {
    // type: 0=base, 1=top, -1=empty
    const empty = '     ';

    if (side === 'left') {
        if (type === 0) return ' [ ] '; // Simple Parcel Base
        if (type === 1) return '  v  '; // Simple Parcel Top
    } else {
        if (type === 0) return ' | | '; // Big Ribbon Base
        if (type === 1) return ' _&_ '; // Big Ribbon Top
    }

    return empty;
}

function shuffle(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
}

function printSky(width, height) {
    // Create empty sky grid
    const sky = [];
    for (let y = 0; y < height; y++) {
        sky[y] = new Array(width).fill(' ');
    }

    // Place Moon ('C')
    // Fixed at top-right, not too close to edge
    const moonX = width - 10;
    const moonY = 2;
    sky[moonY][moonX] = 'C';

    // Place Stars
    // Density: approx 10%
    for (let y = 0; y < height; y++) {
        for (let x = 0; x < width; x++) {
            // Don't overwrite moon
            if (sky[y][x] !== ' ') continue;

            if (Math.random() < 0.05) {
                const rand = Math.random();
                if (rand < 0.7) sky[y][x] = '.';      // Small .
                else if (rand < 0.9) sky[y][x] = '+'; // Big +
                else sky[y][x] = '*';                 // Rare *
            }
        }
    }

    // Print sky
    sky.forEach(row => console.log(row.join('')));
}

function printBanner(width) {
    const text = "MERRY CHRISTMAS !";
    const pattern = ".:*~*:._";

    // Create decoration line of exactly 'width' length
    let decoration = "";
    while (decoration.length < width) {
        decoration += pattern;
    }
    decoration = decoration.slice(0, width);

    // Center text
    const paddingTotal = width - text.length;
    const paddingLeft = Math.floor(paddingTotal / 2);
    // No need for right padding in console.log

    console.log("");
    console.log(decoration);
    console.log("");
    console.log(" ".repeat(paddingLeft) + text);
    console.log("");
    console.log(decoration);
    console.log("");
}

function printTree(height) {
    // Faces pool
    const faces = [' (-.-) ', ' (0.<) ', ' (O.O) ', ' (O.O) '];
    shuffle(faces);

    // Assign random faces
    const leftOuter = faces[0];
    const leftInner = faces[1];
    const rightInner = faces[2];
    const rightOuter = faces[3];

    // Calculate dimensions
    // Side width: Rabbit (14) + Gift (5) = 19
    const sideWidth = 19;
    const maxTreeWidth = 2 * height - 1;
    const totalWidth = sideWidth * 2 + maxTreeWidth;

    // Print Sky
    // Sky height = tree height + 3
    printSky(totalWidth, height + 3);

    // Rabbits sit on the bottom 3 lines:
    // Line height-2: Ears (type 2)
    // Line height-1: Face (type 1)
    // Line trunk   : Feet (type 0)
    // All other lines: Empty (type -1)

    // Gifts sit on the bottom 2 lines (Trunk and Face line)

    for (let i = 0; i < height; i++) {
        const spaces = ' '.repeat(height - i - 1);
        const stars = '*'.repeat(2 * i + 1);
        const treePart = spaces + stars;
        const rightPadding = ' '.repeat(maxTreeWidth - treePart.length);

        let rabbitType = -1;
        if (i === height - 2) rabbitType = 2; // Ears
        if (i === height - 1) rabbitType = 1; // Face

        // Gift logic: Sit on ground (trunk level) and 1 level up (height-1)
        let giftType = -1;
        if (i === height - 1) giftType = 1; // Gift Top

        // Pass faces: for Left (Outer, Inner)
        const leftRabbitRow = getRabbitRow(rabbitType, leftOuter, leftInner);

        // Pass faces: for Right (Inner, Outer)
        const rightRabbitRow = getRabbitRow(rabbitType, rightInner, rightOuter);

        const leftGift = getGiftRow(giftType, 'left');
        const rightGift = getGiftRow(giftType, 'right');

        console.log(leftRabbitRow + leftGift + treePart + rightPadding + rightGift + rightRabbitRow);
    }

    // Trunk line
    const trunkSpaces = ' '.repeat(height - 1);
    const trunkPart = trunkSpaces + '|';
    const trunkRightPadding = ' '.repeat(maxTreeWidth - trunkPart.length);

    // For feet, face args don't matter but needed for function sig
    const leftRabbitRow = getRabbitRow(0, leftOuter, leftInner); // Feet
    const rightRabbitRow = getRabbitRow(0, rightInner, rightOuter); // Feet
    const leftGift = getGiftRow(0, 'left'); // Gift Base
    const rightGift = getGiftRow(0, 'right'); // Gift Base

    console.log(leftRabbitRow + leftGift + trunkPart + trunkRightPadding + rightGift + rightRabbitRow);

    printBanner(totalWidth);
}

printTree(5);
