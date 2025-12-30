Reset = "\x1b[0m"

// Regular Colors
FgBlack = "\x1b[30m"
FgRed = "\x1b[31m"
FgGreen = "\x1b[32m"
FgYellow = "\x1b[33m"
FgBlue = "\x1b[34m"
FgMagenta = "\x1b[35m"
FgCyan = "\x1b[36m"
FgWhite = "\x1b[37m"
FgGray = "\x1b[90m"

// Output Functions
/**
 * 
 * @param {*} color 輸出顏色
 * @param {*} text 輸出文字
 */
function cout(color, text)
{
	console.log(color + "%s" + Reset, text);
}
// Simple, easy-to-read functions to draw a Christmas tree and gifts
function repeat(ch, n) {
	return new Array(n + 1).join(ch);
}

function getStarLines(pad) {
	const left = repeat(' ', pad);
	return [FgYellow + left + '*'+ Reset, FgYellow + left + '***' + Reset];
}

function getTreeLines(levels, trunkHeight) {
	const lines = [];
	for (let i = 0; i < levels; i++) {
		const width = i * 2 + 1;
		const padding = levels - i + 4; // center the tree
		let line = repeat(' ', padding);

		for (let j = 0; j < width; j++) {
			if ((j + i) % 7 === 0) line += FgRed + 'o' + Reset;
			else if ((j + i) % 5 === 0) line += FgMagenta + '●' + Reset;
			else if ((j + i) % 3 === 0) line += FgCyan + '*' + Reset;
			else line += FgGreen + '^' + Reset;
		}

		lines.push(line);
	}

	const trunkPad = levels + 3;
	const trunkLine = repeat(' ', trunkPad) + FgWhite + '|||' + Reset;
	const h = trunkHeight || 2;
	for (let t = 0; t < h; t++) lines.push(trunkLine);
	return lines;
}

function getGiftLinesBoxes() {
	// returns two separate gifts (left and right) as arrays and their widths
	function makeGift(width, height, colorBox, colorRibbon) {
		const out = [];
		const inner = width - 2;
		out.push(colorBox + '┌' + repeat('─', inner) + '┐' + Reset);
		for (let r = 0; r < height - 2; r++) {
			const ribbonPos = Math.floor(inner / 2);
			// left border colored, inner area plain with a colored ribbon, right border colored
			const leftBorder = colorBox + '│' + Reset;
			const rightBorder = colorBox + '│' + Reset;
			const leftSpace = repeat(' ', ribbonPos);
			const rightSpace = repeat(' ', inner - ribbonPos - 1);
			const mid = leftSpace + colorRibbon + '|' + Reset + rightSpace;
			out.push(leftBorder + mid + rightBorder);
		}
		out.push(colorBox + '└' + repeat('─', inner) + '┘' + Reset);
		return out;
	}
	const leftW = 10, rightW = 8, height = 4;
	const g1 = makeGift(leftW, height, FgBlue, FgRed);
	const g2 = makeGift(rightW, height, FgMagenta, FgYellow);

	return {left: g1, right: g2, leftW: leftW, rightW: rightW, height: height};
}

// Compose the scene and print with gifts beside the trunk
function showChristmas() {
	// prepare gifts (left and right)
	const gifts = getGiftLinesBoxes();
	const leftGift = gifts.left;
	const rightGift = gifts.right;
	const leftW = gifts.leftW;
	const rightW = gifts.rightW;

	// ensure tree base width is wider than combined gifts + trunk
	const trunkW = 3;
	let levels = 6;
	while ((levels * 2 - 1) <= (leftW + trunkW + rightW)) levels++;

	const trunkHeight = Math.max(2, gifts.height);

	// raw star shape lines (will be centered and colored when printing)
	const rawStarLines = [
		'   *   ',
		'  * *  ',
		' * * * ',
		'*  *  *',
		' * * * '
	];

	// small white snowman (3 lines)
	const snow = [
		FgWhite + '  _===_' + Reset,
		FgWhite + ' (.,.) ' + Reset,
		FgWhite + ' ( : ) ' + Reset
	];

	const trunkTopIndex = levels; // 0-based index where trunk starts
	const giftTopIndex = trunkTopIndex;

	// build tree lines per frame to allow blinking
	function buildTreeLines(frame) {
		const lines = [];
		for (let i = 0; i < levels; i++) {
			const width = i * 2 + 1;
			const padding = levels - i + 4; // center the tree
			let line = repeat(' ', padding);

			for (let j = 0; j < width; j++) {
				let ch = '^';
				let color = FgGreen;
				if ((j + i) % 7 === 0) { ch = 'o'; color = FgRed; }
				else if ((j + i) % 5 === 0) { ch = '●'; color = FgMagenta; }
				else if ((j + i) % 3 === 0) { ch = '*'; color = FgCyan; }

				if (ch !== '^') {
					// deterministic-ish flicker: depends on frame and position
					const on = ((frame + i * 7 + j * 13) % 6) < 3; // on for half the cycle
					if (on) line += color + ch + Reset;
					else line += FgGreen + '^' + Reset; // show branch when ornament is off (more visible)
				} else {
					line += color + ch + Reset;
				}
			}

			lines.push(line);
		}

		const trunkPad = levels + 3;
		const trunkLine = repeat(' ', trunkPad) + FgWhite + '|||' + Reset;
		const h = trunkHeight || 2;
		for (let t = 0; t < h; t++) lines.push(trunkLine);
		return lines;
	}

	// animation loop
	let frame = 0;
	const intervalMs = 400;

	function render() {
		console.clear();
		const treeLines = buildTreeLines(frame);

		const totalLines = Math.max(treeLines.length, giftTopIndex + Math.max(leftGift.length, rightGift.length));

		// print star centered relative to tree area, including gift placeholders
		const treeLeftPad = levels - (levels - 1) + 4; // same formula as in getTreeLines bottom padding
		const treeBottomWidth = levels * 2 - 1;
		const starWidthCalc = 7;
		const starInnerPad = treeLeftPad + Math.floor((treeBottomWidth - starWidthCalc) / 2);
		const lgPlaceholder = repeat(' ', leftW);
		const rgPlaceholder = repeat(' ', rightW);

		// draw star (blink every other frame)
		const starColor = (frame % 2 === 0) ? FgYellow : FgGray;
		for (const s of rawStarLines) {
			const starLine = lgPlaceholder + ' ' + repeat(' ', starInnerPad) + starColor + s + Reset + ' ' + rgPlaceholder;
			cout('', starLine);
		}

		// place snow so its bottom aligns with tree base
		const snowTop = Math.max(0, treeLines.length - snow.length);

		for (let i = 0; i < totalLines; i++) {
			const lg = (i - giftTopIndex >= 0 && i - giftTopIndex < leftGift.length) ? leftGift[i - giftTopIndex] : repeat(' ', leftW);
			const rg = (i - giftTopIndex >= 0 && i - giftTopIndex < rightGift.length) ? rightGift[i - giftTopIndex] : repeat(' ', rightW);
			const tree = treeLines[i] || repeat(' ', treeLines[0].length);
			const snowLine = (i >= snowTop && i < snowTop + snow.length) ? snow[i - snowTop] : '';
			cout('', lg + ' ' + tree + ' ' + rg + ' ' + snowLine);
		}

		frame++;
	}

	render();
    // Animate or static display
	// setInterval(render, intervalMs);
}

// Run
showChristmas();

