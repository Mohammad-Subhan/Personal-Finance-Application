import { useState } from "react"
import Layout from "@/components/layout"
import { ArrowDownIcon, ArrowUpIcon, Download } from "lucide-react"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"

function WalletPage() {
    const [isDialogOpen, setIsDialogOpen] = useState(false)
    const [amount, setAmount] = useState("")
    const [type, setType] = useState("")
    const [description, setDescription] = useState("")
    const [spPerson, setspPerson] = useState("")

    const handleSubmit = (e) => {
        e.preventDefault()
        console.log("Transaction:", { amount, type, description })
        setIsDialogOpen(false)
        // Here you would typically send this data to your backend
    }

    return (
        <Layout>
            <div className="container p-4 max-w-full space-y-4">
                <div className="flex justify-center items-center">
                    <Card className="bg-red-300 border-none w-4/5 h-[190px] p-4 text-background rounded-[35px]">
                        <div className="w-full h-full bg-red-500 rounded-[22px] p-4">
                            <div className="flex justify-between items-start">
                                <div className="space-y-4">
                                    <h2 className="text-lg font-medium opacity-90">Bank Alfalah</h2>
                                    <div className="pt-7">
                                        <p className="text-sm opacity-80">Balance</p>
                                        <p className="text-3xl font-bold">Rs. 174,000.00</p>
                                    </div>
                                </div>
                                <Button variant="ghost" className="text-background hover:text-white/90 p-2">
                                    <Download className="h-6 w-6" />
                                </Button>
                            </div>
                        </div>
                    </Card>
                </div>
                <div className="flex justify-end">
                    <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
                        <DialogTrigger asChild>
                            <Button className="bg-primary hover:bg-primaryHover text-background">Add Transaction</Button>
                        </DialogTrigger>
                        <DialogContent className="sm:max-w-[425px]">
                            <DialogHeader>
                                <DialogTitle>Add Transaction</DialogTitle>
                            </DialogHeader>
                            <form onSubmit={handleSubmit} className="space-y-4">
                                <div className="space-y-2">
                                    <Label htmlFor="amount">Amount</Label>
                                    <Input
                                        id="amount"
                                        type="number"
                                        min="0"
                                        value={amount}
                                        onChange={(e) => setAmount(e.target.value)}
                                        placeholder="Enter amount"
                                    />
                                </div>
                                <div className="space-y-2">
                                    <Label htmlFor="type">Transaction Category</Label>
                                    <Select onValueChange={setType} value={type}>
                                        <SelectTrigger id="type">
                                            <SelectValue placeholder="Select category" />
                                        </SelectTrigger>
                                        <SelectContent className="bg-background">
                                            <SelectItem className="hover:cursor-pointer hover:bg-gray-50" value="food">Food</SelectItem>
                                            <SelectItem className="hover:cursor-pointer hover:bg-gray-50" value="entertainment">Entertainment</SelectItem>
                                        </SelectContent>
                                    </Select>
                                </div>
                                <div className="space-y-2">
                                    <Label htmlFor="type">Transaction Type</Label>
                                    <Select onValueChange={setType} value={type}>
                                        <SelectTrigger id="type">
                                            <SelectValue placeholder="Select type" />
                                        </SelectTrigger>
                                        <SelectContent className="bg-background">
                                            <SelectItem className="hover:cursor-pointer hover:bg-gray-50" value="credit">Credit</SelectItem>
                                            <SelectItem className="hover:cursor-pointer hover:bg-gray-50" value="debit">Debit</SelectItem>
                                        </SelectContent>
                                    </Select>
                                </div>
                                <div className="space-y-2">
                                    <Label htmlFor="description">Description</Label>
                                    <Input
                                        id="description"
                                        value={description}
                                        onChange={(e) => setDescription(e.target.value)}
                                        placeholder="Enter description"
                                    />
                                </div>
                                <div className="space-y-2">
                                    <Label htmlFor="description">Second Person</Label>
                                    <Input
                                        id="spPerson"
                                        value={spPerson}
                                        onChange={(e) => setspPerson(e.target.value)}
                                        placeholder="Enter second person"
                                    />
                                </div>
                                <Button type="submit" className="w-full">
                                    Save
                                </Button>
                            </form>
                        </DialogContent>
                    </Dialog>
                </div>

                <div className="space-y-2">
                    <Card className="p-4 flex items-center justify-between hover:bg-slate-50 transition-colors">
                        <div className="flex items-center gap-3">
                            <div className="bg-green-100 p-2 rounded-full">
                                <ArrowDownIcon className="h-4 w-4 text-primary" />
                            </div>
                            <div>
                                <p className="font-medium">Salary</p>
                                <p className="text-sm text-slate-500">Today, 2:45 PM</p>
                            </div>
                        </div>
                        <p className="text-primary font-medium">+Rs. 50,000.00</p>
                    </Card>

                    <Card className="p-4 flex items-center justify-between hover:bg-slate-50 transition-colors">
                        <div className="flex items-center gap-3">
                            <div className="bg-red-100 p-2 rounded-full">
                                <ArrowUpIcon className="h-4 w-4 text-red-600" />
                            </div>
                            <div>
                                <p className="font-medium">Groceries</p>
                                <p className="text-sm text-slate-500">Yesterday, 5:30 PM</p>
                            </div>
                        </div>
                        <p className="text-red-600 font-medium">-Rs. 2,500.00</p>
                    </Card>
                </div>
            </div>
        </Layout>
    )
}

export default WalletPage;