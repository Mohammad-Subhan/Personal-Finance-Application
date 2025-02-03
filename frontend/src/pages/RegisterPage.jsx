import { Card, CardContent } from "@/components/ui/card"
import { Link } from "react-router-dom"
import RegisterForm from "@/components/RegisterForm"

export default function RegisterPage() {
    return (
        <div className="min-h-screen grid lg:grid-cols-2">
            <div className="hidden lg:flex flex-col items-center justify-center bg-primary p-8 text-text">
                <h1 className="text-5xl text-background font-bold mb-4">Company Logo</h1>
                <p className="text-xl text-background">Welcome to our platform</p>
            </div>
            <div className="flex items-center justify-center p-8">
                <Card className="w-full max-w-md">
                    <CardContent className="pt-6">
                        <div className="mb-6">
                            <h2 className="text-3xl font-bold mb-2">Register</h2>
                        </div>
                        <RegisterForm />
                        <div className="mt-6 text-center text-sm">
                            Already have an account?{" "}
                            <Link to="/login" className="text-primary hover:underline">
                                Login
                            </Link>
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    )
}