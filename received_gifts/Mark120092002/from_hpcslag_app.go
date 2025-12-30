package main

import (
	"fmt"
	"math"
	"time"
)

const (
	W = 80
	H = 40
)

type Vec3 struct {
	x, y, z float64
}

func rotateY(v Vec3, a float64) Vec3 {
	c, s := math.Cos(a), math.Sin(a)
	return Vec3{
		x: v.x*c + v.z*s,
		y: v.y,
		z: -v.x*s + v.z*c,
	}
}

func project(v Vec3) (int, int, float64) {
	depth := v.z + 25
	scale := 20 / depth
	x := int(v.x*scale) + W/2
	y := int(v.y*scale) + H/2
	return x, y, depth
}

func clear() {
	fmt.Print("\033[H\033[2J")
}

func buildTree() []Vec3 {
	var pts []Vec3
	h := 14.0

	for y := 0.0; y < h; y += 0.4 {
		r := (h - y) / h * 6
		for a := 0.0; a < math.Pi*2; a += 0.25 {
			x := math.Cos(a)*r + 0.6 // 偏心！
			z := math.Sin(a) * r
			pts = append(pts, Vec3{x, -y, z})
		}
	}

	// 樹幹
	for y := 0.0; y < 3; y += 0.3 {
		pts = append(pts, Vec3{0, y, 0})
	}

	return pts
}

func shade(z float64) rune {
	switch {
	case z < 18:
		return '#'
	case z < 20:
		return '*'
	case z < 23:
		return '+'
	default:
		return '.'
	}
}

func main() {
	tree := buildTree()
	angle := 0.0

	go (func() {
		for {
			buf := make([][]rune, H)
			zbuf := make([][]float64, H)
			for y := 0; y < H; y++ {
				buf[y] = make([]rune, W)
				zbuf[y] = make([]float64, W)
				for x := 0; x < W; x++ {
					buf[y][x] = ' '
					zbuf[y][x] = math.MaxFloat64
				}
			}

			for _, p := range tree {
				r := rotateY(p, angle)
				x, y, z := project(r)
				if x >= 0 && x < W && y >= 0 && y < H {
					if z < zbuf[y][x] {
						zbuf[y][x] = z
						buf[y][x] = shade(z)
					}
				}
			}

			clear()
			for _, row := range buf {
				fmt.Println(string(row))
			}

			angle += 0.08
			time.Sleep(40 * time.Millisecond)
		}
	})()

	time.Sleep(10 * time.Second)
}
