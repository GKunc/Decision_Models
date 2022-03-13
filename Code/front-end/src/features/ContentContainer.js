import FileUpload from "./FileUpload";

export default function ContentContainer(props) {
    return (
        <div className="flex flex-col h-full text-white m-2">
            <FileUpload />
        </div>
    );
}