import { Plus } from "lucide-react"
import { FaWallet } from "react-icons/fa";
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import DashboardChart from "@/components/DashboardChart"
import Layout from "@/components/Layout"
export default function DashboardPage() {
    return (
        <Layout>
            <div className="container max-w-full p-6 mx-auto space-y-6">
                <div className="grid grid-cols-4 gap-4">
                    <Card className="col-span-1 p-4 bg-primaryAccent text-white rounded-[35px]">
                        <div className="w-full h-full bg-primary rounded-[22px] p-4">
                            <div className="space-y-1 h-4/5 w-4/5">
                                <h2 className="text-xl font-medium pb-[125px]">Mohammad Subhan Khalid</h2>
                                <div className="space-y-1">
                                    <p className="text-sm text-emerald-100">Wallets:</p>
                                    <p className="text-lg font-bold">3</p>
                                </div>
                                <div className="space-y-1">
                                    <p className="text-sm text-emerald-100">Balance</p>
                                    <p className="text-3xl font-bold">Rs. 1740.00</p>
                                </div>
                            </div>
                        </div>
                    </Card>
                    <Card className="col-span-3 p-4">
                        <DashboardChart />
                    </Card>
                </div>

                <Button className="bg-primary hover:bg-primaryHover text-background">
                    <Plus className="w-4 h-4 mr-2" />
                    Add Wallet
                </Button>

                <div className="grid gap-4 md:grid-cols-3">
                    <Button variant="outline" className="h-28 bg-white drop-shadow-md hover:drop-shadow-xl border text-white">
                        <FaWallet />
                    </Button>
                    <Button variant="outline" className="h-28 bg-white drop-shadow-md hover:drop-shadow-xl border text-white">
                    </Button>
                    <Button variant="outline" className="h-28 bg-white drop-shadow-md hover:drop-shadow-xl border text-white">
                    </Button>
                </div>
            </div>
        </Layout>
    )
}