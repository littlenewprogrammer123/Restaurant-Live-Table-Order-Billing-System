import { useEffect, useState } from "react";
import Layout from "../components/Layout";
import api from "../api";
import { useAuth } from "../context/AuthContext";

function Cashier() {
  const { user } = useAuth();
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);

  // -------------------------
  // LOAD BILL REQUESTED ORDERS
  // -------------------------
  const loadOrders = async () => {
    try {
      const res = await api.get("/orders/");
      const billRequested = res.data.filter(
        (o) => o.status === "BILL_REQUESTED"
      );
      setOrders(billRequested);
    } catch (err) {
      console.error(err);
      alert("Failed to load orders");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadOrders();
  }, []);

  // -------------------------
  // TOTAL CALCULATION
  // -------------------------
  const calculateTotal = (items) => {
    return items.reduce(
      (sum, item) =>
        sum + item.menu_item.price * item.quantity,
      0
    );
  };

  // -------------------------
  // PAY & CLOSE
  // -------------------------
  const closeOrder = async (orderId) => {
    if (!window.confirm("Confirm payment received?")) return;

    try {
      await api.post(`/orders/${orderId}/close/`);
      loadOrders();
    } catch {
      alert("Failed to close order");
    }
  };

  // -------------------------
  // ACCESS CONTROL
  // -------------------------
  if (!user || user.role !== "CASHIER") {
    return <div className="p-3">Access denied</div>;
  }

  if (loading) {
    return <div className="p-3">Loading billing screen...</div>;
  }

  return (
    <Layout>
      <h4 className="mb-3">Cashier Billing</h4>

      {orders.length === 0 && (
        <div className="alert alert-info">
          No bills pending
        </div>
      )}

      {orders.map((order) => (
        <div key={order.id} className="card mb-4 p-3">
          <div className="d-flex justify-content-between align-items-center mb-2">
            <strong>
              Table {order.table_number} — Order #{order.id}
            </strong>
            <span className="badge bg-warning text-dark">
              BILL REQUESTED
            </span>
          </div>

          <table className="table table-sm">
            <thead>
              <tr>
                <th>Item</th>
                <th>Qty</th>
                <th>Price</th>
                <th>Total</th>
              </tr>
            </thead>
            <tbody>
              {order.items.map((item) => (
                <tr key={item.id}>
                  <td>{item.menu_item.name}</td>
                  <td>{item.quantity}</td>
                  <td>₹{item.menu_item.price}</td>
                  <td>
                    ₹{item.menu_item.price * item.quantity}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          <div className="d-flex justify-content-between align-items-center">
            <h5>
              Total: ₹{calculateTotal(order.items)}
            </h5>
            <button
              className="btn btn-success"
              onClick={() => closeOrder(order.id)}
            >
              Pay & Close
            </button>
          </div>
        </div>
      ))}
    </Layout>
  );
}

export default Cashier;
