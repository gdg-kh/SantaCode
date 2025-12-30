use std::io::{self, Write};
use std::thread;
use std::time::{Duration, SystemTime, UNIX_EPOCH};

struct LcgRng {
    state: u64,
}

impl LcgRng {
    // Pseudo-Random Number Generator via the Linear Congruential Generator (LCG) since we cannot use the 'rand' crate.
    fn new() -> Self {
        let start = SystemTime::now();
        let since_epoch = start.duration_since(UNIX_EPOCH).unwrap_or(Duration::ZERO);
        Self {
            state: since_epoch.as_nanos() as u64,
        }
    }

    fn next(&mut self) -> u64 {
        self.state = self.state.wrapping_mul(6364136223846793005).wrapping_add(1);
        self.state
    }

    fn gen_range(&mut self, min: usize, max: usize) -> usize {
        if min >= max {
            return min;
        }
        let range = (max - min) as u64;
        let rnd = self.next();
        (min as u64 + (rnd % range)) as usize
    }

    fn gen_ratio(&mut self, numerator: u32, denominator: u32) -> bool {
        if denominator == 0 {
            return false;
        }
        (self.next() % denominator as u64) < numerator as u64
    }
}

// ANSI Escape Codes
const ESC: &str = "\x1b";
const HIDE_CURSOR: &str = "\x1b[?25l";
const SHOW_CURSOR: &str = "\x1b[?25h";
const CLEAR_SCREEN: &str = "\x1b[2J";
const RESET_COLOR: &str = "\x1b[0m";

// Colors
const COLOR_RED: &str = "\x1b[31m";
const COLOR_GREEN: &str = "\x1b[32m";
const COLOR_YELLOW: &str = "\x1b[33m";
const COLOR_BLUE: &str = "\x1b[34m";
const COLOR_MAGENTA: &str = "\x1b[35m";
const COLOR_CYAN: &str = "\x1b[36m";
const COLOR_WHITE: &str = "\x1b[37m";
const COLOR_DARK_GREEN: &str = "\x1b[38;5;22m"; // Extended 256 color for darker green
const COLOR_DARK_GREY: &str = "\x1b[90m";
const COLOR_GOLD: &str = "\x1b[38;5;220m"; // Extended 256 color for gold

fn move_to(w: &mut impl Write, x: u16, y: u16) -> io::Result<()> {
    // ANSI uses 1-based indexing: ESC [ <row> ; <col> H
    write!(w, "\x1b[{};{}H", y + 1, x + 1)
}

fn set_color(w: &mut impl Write, color_code: &str) -> io::Result<()> {
    write!(w, "{}", color_code)
}

fn reset_color(w: &mut impl Write) -> io::Result<()> {
    write!(w, "{}", RESET_COLOR)
}

const TREE: &[&str] = &[
    "        ★        ",
    "        ▲        ",
    "       /█\\       ",
    "      /███\\      ",
    "     /█████\\     ",
    "    /███████\\    ",
    "   /█████████\\   ",
    "  /███████████\\  ",
    " /█████████████\\ ",
    "/███████████████\\",
    "       ███       ",
    "       ███       ",
];

const ORNAMENT_POSITIONS: &[(usize, usize)] = &[
    (3, 8),
    (4, 7),
    (4, 9),
    (5, 6),
    (5, 10),
    (5, 8),
    (6, 5),
    (6, 9),
    (6, 11),
    (7, 4),
    (7, 8),
    (7, 12),
    (8, 3),
    (8, 7),
    (8, 11),
    (8, 15),
    (9, 2),
    (9, 6),
    (9, 10),
    (9, 14),
];

const SNOWFLAKES: &[char] = &['❄', '❅', '❆', '*', '·', '•', '✦'];

struct Snowflake {
    x: u16,
    y: u16,
    symbol: char,
    speed: u8,
}

fn main() -> io::Result<()> {
    let mut stdout = io::stdout();
    // note: we can't reliably get terminal size without libc/crossterm in pure std.
    // We will assume a reasonable default or try to rely on user resizing.
    // For this demo, let's hardcode a "virtual" canvas size or just draw absolutely assuming typical size.
    // Since snowflakes need bounds, let's assume standard 80x24 for safety,
    // or try a trick. But standard 80x24 is safest for "no dependencies".
    let width: u16 = 80;
    let height: u16 = 18;

    // Setup terminal
    write!(stdout, "{}{}{}", ESC, HIDE_CURSOR, CLEAR_SCREEN)?;

    let mut rng = LcgRng::new();
    let mut snowflakes: Vec<Snowflake> = Vec::new();
    let mut frame = 0u64;
    let mut star_bright = true;

    let tree_x = (width / 2).saturating_sub(9);
    let tree_y = (height / 2).saturating_sub(8);

    let start_time = SystemTime::now();

    loop {
        // Run for exactly 4 seconds only
        if start_time.elapsed().unwrap_or(Duration::ZERO) >= Duration::from_secs(4) {
            break;
        }

        // To reduce flicker, we could just overwrite, but clearing is safer for artifacts.
        write!(stdout, "{}", CLEAR_SCREEN)?;

        // --- LAYER 0: BORDER & GROUND ---
        set_color(&mut stdout, COLOR_DARK_GREY)?;
        // Top & Bottom Border
        for col in 0..width {
            move_to(&mut stdout, col, 0)?;
            write!(stdout, "═")?;
            move_to(&mut stdout, col, height - 1)?;
            write!(stdout, "═")?;
        }
        // Left & Right Border
        for row in 0..height {
            move_to(&mut stdout, 0, row)?;
            write!(stdout, "║")?;
            move_to(&mut stdout, width - 1, row)?;
            write!(stdout, "║")?;
        }
        // Corners
        move_to(&mut stdout, 0, 0)?;
        write!(stdout, "╔")?;
        move_to(&mut stdout, width - 1, 0)?;
        write!(stdout, "╗")?;
        move_to(&mut stdout, 0, height - 1)?;
        write!(stdout, "╚")?;
        move_to(&mut stdout, width - 1, height - 1)?;
        write!(stdout, "╝")?;

        // Snowflakes
        for flake in &snowflakes {
            // Keep flakes inside border (1 to width-2, 1 to height-2)
            if flake.x > 0 && flake.x < width - 1 && flake.y > 0 && flake.y < height - 1 {
                move_to(&mut stdout, flake.x, flake.y)?;
                set_color(&mut stdout, COLOR_WHITE)?;
                write!(stdout, "{}", flake.symbol)?;
                reset_color(&mut stdout)?;
            }
        }

        // Tree
        for (i, line) in TREE.iter().enumerate() {
            let y = tree_y + i as u16;
            for (j, ch) in line.chars().enumerate() {
                let x = tree_x + j as u16;
                if x < width && y < height {
                    let color = match ch {
                        '★' => {
                            if star_bright {
                                COLOR_YELLOW
                            } else {
                                COLOR_GOLD
                            }
                        }
                        '█' | '▲' => COLOR_GREEN,
                        '/' | '\\' => COLOR_DARK_GREEN,
                        _ => RESET_COLOR,
                    };

                    if ch != ' ' {
                        move_to(&mut stdout, x, y)?;
                        set_color(&mut stdout, color)?;
                        write!(stdout, "{}", ch)?;
                        reset_color(&mut stdout)?;
                    }
                }
            }
        }

        // Ornaments
        let ornament_colors = [
            COLOR_RED,
            COLOR_BLUE,
            COLOR_YELLOW,
            COLOR_MAGENTA,
            COLOR_CYAN,
        ];
        for (idx, &(row, col)) in ORNAMENT_POSITIONS.iter().enumerate() {
            let x = tree_x + col as u16;
            let y = tree_y + row as u16;
            if x < width && y < height {
                let color_idx = (idx + frame as usize / 3) % ornament_colors.len();
                let symbol = if (frame as usize + idx) % 4 == 0 {
                    '●'
                } else {
                    '○'
                };

                move_to(&mut stdout, x, y)?;
                set_color(&mut stdout, ornament_colors[color_idx])?;
                write!(stdout, "{}", symbol)?;
                reset_color(&mut stdout)?;
            }
        }

        // Message
        let messages = [
            "✨ Merry Christmas! ✨",
            "✨ Greeting from Malaysia, by Aaron ✨",
        ];
        let msg = messages[(frame as usize / 25) % messages.len()];
        let msg_x = (width / 2).saturating_sub(msg.chars().count() as u16 / 2);
        let msg_y = tree_y + TREE.len() as u16 + 2;
        if msg_y < height {
            move_to(&mut stdout, msg_x, msg_y)?;
            set_color(&mut stdout, COLOR_GOLD)?;
            write!(stdout, "{}", msg)?;
            reset_color(&mut stdout)?;
        }

        stdout.flush()?;

        // Snowflakes gen.
        snowflakes.retain_mut(|flake| {
            if frame % flake.speed as u64 == 0 {
                flake.y += 1;
                let rnd = rng.gen_range(0, 3) as i32 - 1; // -1, 0, 1
                flake.x = ((flake.x as i32 + rnd).max(0) as u16).min(width - 1);
            }
            flake.y < height
        });

        if rng.gen_ratio(1, 3) {
            snowflakes.push(Snowflake {
                x: rng.gen_range(0, width as usize) as u16,
                y: 0,
                symbol: SNOWFLAKES[rng.gen_range(0, SNOWFLAKES.len())],
                speed: rng.gen_range(1, 4) as u8,
            });
        }

        if frame % 5 == 0 {
            star_bright = !star_bright;
        }

        frame += 1;
        thread::sleep(Duration::from_millis(80));
    }

    // Cleanup
    move_to(&mut stdout, 0, height)?;
    write!(stdout, "{}{}\n", SHOW_CURSOR, RESET_COLOR)?;
    Ok(())
}

