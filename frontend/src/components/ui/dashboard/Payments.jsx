import { FiCreditCard, FiPlus, FiSmartphone } from 'react-icons/fi'
import PaymentMethodCard from './PaymentMethodCard'
import TransactionTable from './TransactionTable'

const Payments = () => {
  const paymentMethods = [
    { id: 1, type: 'UPI', icon: <FiSmartphone className="h-6 w-6 text-purple-600" />, lastFour: 'upi@example' },
    { id: 2, type: 'Credit Card', icon: <FiCreditCard className="h-6 w-6 text-blue-600" />, lastFour: '4242' },
    { id: 3, type: 'Net Banking', icon: <FiCreditCard className="h-6 w-6 text-green-600" />, lastFour: 'HDFC' },
  ]

  const transactions = [
    { id: 'txn_1', date: '2023-05-15', course: 'Blockchain Fundamentals', amount: '₹4,500', status: 'Completed', method: 'UPI', txHash: '0x123...456' },
    { id: 'txn_2', date: '2023-05-10', course: 'Smart Contracts', amount: '₹3,000', status: 'Completed', method: 'Credit Card', txHash: '0x789...012' },
    { id: 'txn_3', date: '2023-05-05', course: 'Web Development', amount: '₹3,500', status: 'Completed', method: 'Net Banking', txHash: '0x345...678' },
    { id: 'txn_4', date: '2023-05-01', course: 'Advanced Solidity', amount: '₹1,500', status: 'Failed', method: 'UPI', txHash: '0x901...234' },
  ]

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row md:items-center md:justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Payments</h1>
        <button className="mt-4 md:mt-0 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
          Make New Payment
        </button>
      </div>
      
      {/* Payment methods */}
      <div>
        <h2 className="text-lg font-medium text-gray-900 mb-4">Payment Methods</h2>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {paymentMethods.map((method) => (
            <PaymentMethodCard key={method.id} method={method} />
          ))}
          <div className="bg-white overflow-hidden shadow rounded-lg border-2 border-dashed border-gray-300 hover:border-indigo-500 flex items-center justify-center cursor-pointer">
            <div className="px-4 py-5 sm:p-6 text-center">
              <div className="flex items-center justify-center h-12 w-12 rounded-full bg-indigo-100 mx-auto">
                <FiPlus className="h-6 w-6 text-indigo-600" />
              </div>
              <h3 className="mt-2 text-sm font-medium text-gray-900">Add new method</h3>
              <p className="mt-1 text-sm text-gray-500">Connect UPI, card or bank account</p>
            </div>
          </div>
        </div>
      </div>
      
      {/* Transaction history */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-medium text-gray-900">Transaction History</h2>
          <div className="flex space-x-2">
            <select className="block pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md">
              <option>All Methods</option>
              <option>UPI</option>
              <option>Credit Card</option>
              <option>Net Banking</option>
            </select>
            <select className="block pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md">
              <option>All Statuses</option>
              <option>Completed</option>
              <option>Pending</option>
              <option>Failed</option>
            </select>
          </div>
        </div>
        <TransactionTable transactions={transactions} />
      </div>
    </div>
  )
}

export default Payments