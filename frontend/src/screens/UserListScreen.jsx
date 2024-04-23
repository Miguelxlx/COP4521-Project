import { LinkContainer } from "react-router-bootstrap"
import { Table, Button } from "react-bootstrap"
import { FaTimes, FaEdit, FaCheck, FaTrash } from "react-icons/fa"
import Message from "../components/Message"
import Loader from "../components/Loader"
//import { useGetUsersQuery, useDeleteUserMutation } from "../slices/usersApiSlice"
//import { Link } from "react-router-dom"
import { toast } from 'react-toastify'
import { useEffect, useState } from "react"
//import { useSelector } from 'react-redux'
const UserListScreen = () => {
    const [users, setUsers] = useState([]);
    //const userInfo = useSelector(state => state.auth.userInfo);

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    useEffect(() => {
        fetchUsers();
    }, []);

    const fetchUsers = async () => {
        setLoading(true);
        try {
            const response = await fetch("http://127.0.0.1:5000/user_list");
            const data = await response.json();
            if (response.ok) {
                setUsers(data.users);
            } else {
                console.error("Failed to fetch users");
                setError(data.message)
            }
        } catch (error) {
            console.error("Error fetching users list:", error);
        } finally {
            setLoading(false);
        }
    }
    
    const deleteHandler = async (id) => {
        if(window.confirm('Are you sure?')) { 
            try {
            const response = await fetch("http://127.0.0.1:5000/delete_user", {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ id: id }),
            });
            //const data = await response.json()
            if (response.ok) {
                toast.success('User deleted')
                fetchUsers();
            }
            } catch (err) {
                toast.error(err?.data?.message || err.error);
            }
    }
    }

  return (
    <>
    <h1>Users</h1>
    {loading ? <Loader /> : error ? <Message variant='danger'>{error}
    </Message> : (
        <Table striped hover responsive className='table-sm'>

            <thead>
                <tr>
                    <th>ID</th>
                    <th>NAME</th>
                    <th>EMAIL</th>
                    <th>ADMIN</th>
                    <th></th>
                </tr>
            </thead>
            <tbody>
                { users.map((user) => (
                    <tr key={user._id}>
                        <td>{user._id}</td>
                        <td>{user.name}</td>
                        <td><a href={`mailto:${user.email}`}>{ user.email }</a></td>
                        <td>
                        { user.role === 'admin' ? (
                            <FaCheck style={{ color: 'green' }} />
                        ) : (
                            <FaTimes style={{ color: 'red' }} />
                        )}
                        </td>
                        <td>
                            <LinkContainer to={`/admin/user/${user._id}/edit`}>
                                <Button variant='light' className='btn-sm'>
                                    <FaEdit />
                                </Button>
                            </LinkContainer>
                            <Button variant='danger' className='btn-sm' onClick={() => deleteHandler(user._id)}>
                                <FaTrash style={{ color: 'white' }} />
                            </Button>
                        </td>
                    </tr>
                ))}
            </tbody>
        </Table>
    )}
    </>
  )
}

export default UserListScreen