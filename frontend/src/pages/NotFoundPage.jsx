import { Link } from "react-router-dom"
import { Button } from "@/components/ui/button"

export default function NotFoundPage() {
    return (
        <div className="min-h-screen flex flex-col items-center justify-center bg-background p-8">
            <div className="text-center">
                <h1 className="text-9xl font-bold bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">404</h1>
                <h2 className="text-3xl font-bold mt-4 mb-2">Page Not Found</h2>
                <p className="text-gray-600 mb-8">The page you are looking for doesn&apos;t exist or has been moved.</p>
                <Button asChild className="bg-primary hover:bg-primaryHover text-background">
                    <Link href="/">Return Dashboard</Link>
                </Button>
            </div>
        </div>
    )
}