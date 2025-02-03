import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

function LoginForm() {
    return (
        <form className="space-y-4">
            <div className="space-y-2">
                <Label htmlFor="username">Username</Label>
                <Input id="username" placeholder="Enter your username" required />
            </div>
            <div className="space-y-2">
                <Label htmlFor="password">Password</Label>
                <Input id="password" type="password" placeholder="Enter your password" required />
            </div>
            <Button className="w-full bg-primary hover:bg-primaryHover text-background" type="submit">
                Login
            </Button>
        </form>
    );
}

export default LoginForm;