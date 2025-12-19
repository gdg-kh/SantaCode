import Foundation

precedencegroup PipeRight {
    associativity: left
    higherThan: AssignmentPrecedence
}

infix operator |> : PipeRight

public
func |> <T, U>(value: T, function: (T) -> U) -> U
{
    function(value)
}

struct Seed
{
    let height: Int
}

func seed() -> (Int) -> Seed
{
    {
        Seed(height: $0)
    }
}

func watering() -> (Seed) -> String
{
    {
        seed in
        
        let emojiLeaves: Array<String> = "🍏🍎🍐🍊🍋🍓🍈🍑🥭🫑".map(String.init)
        let result = (0 ..< seed.height).map {
            
            layer in
            
            let spaces = String(repeating: " ", count: seed.height - layer - 1)
            let leave: (Int) -> String = {
                
                if $0 == 0 {
                    
                    return "🌟"
                }
                
                return emojiLeaves.randomElement() ?? "🍏"
            }
            let leaves: String = (0 ..< (layer + 1)).map { _ in leave(layer) }.joined()
            
            return spaces + leaves
        }
        
        return result.joined(separator: "\n")
    }
}

func grow() -> (String) -> Void
{
    {
        plant in
        
        let count: Int = plant.split(separator: "\n").count - 1
        var result: String = plant + "\n" + String(repeating: " ", count: count) + "🟫"
        
        if count >= 3 {
            
            result += "\n" + String(repeating: " ", count: count - 2) + "🟫🟫🟫"
        }
        
        result += "\nMerry Christmas! 🎄"
        
        print(result)
    }
}

5 |> seed() |> watering() |> grow()